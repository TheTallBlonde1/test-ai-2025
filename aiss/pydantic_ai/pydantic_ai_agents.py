"""Pydantic AI multi-agent orchestration example.

This module demonstrates an agentic approach to produce the same structured
outputs as `aiss.openai_direct.openai_parsed.get_parsed_response`, but using
multiple Pydantic AI agents with distinct roles:

- Model detection agent: infers the appropriate `ModelType` from free text
- Wikipedia agent: fetches background context about the topic
- Domain specialists (history, researcher, critic, summarizer, business analyst)
  provide targeted narrative/context used to prime the final formatting agent
- Formatting agent: outputs the Pydantic model instance for the detected type

All agents include background role prompts to guide behavior. The orchestrator
`run_agents_parsed` composes their outputs to produce and render the final
structured result.
"""

from __future__ import annotations

import os
from typing import Optional, Sequence, Type, TypeVar, cast

from pydantic import BaseModel, Field
from rich.console import Console
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from aiss.models.protocols import ModelFormatProtocol
from aiss.models.shared import ModelType, ModelTypeInput

# Import pydantic_ai lightly so tests can patch Agent; don't hard-fail if missing
try:  # pragma: no cover - exercised via test mocks
    from pydantic_ai import Agent, RunContext
except Exception:  # pragma: no cover
    Agent = None  # type: ignore
    RunContext = object  # type: ignore


T = TypeVar("T", bound=ModelFormatProtocol)


def _provider_model_name() -> str:
    base = os.getenv("OPENAI_MODEL_NAME", "gpt-5-mini").strip()
    return base if ":" in base else f"openai:{base}"


# ---------- Detection ----------
class DetectionOutput(BaseModel):
    """Pydantic output for model detection agent."""

    model_type: str = Field(description="Detected model type key; must be one of ModelType.registry() keys")
    formatted_name: str = Field(description="Normalized name/title for the work")
    description: str = Field(description="Short description of the work")
    additional_info: list[str] | None = Field(default=None, description="Optional extra hints like year, platform, etc.")


def _detection_instructions() -> str:
    return f"You are an expert classifier for entertainment content (shows, movies, games).\nGiven the user's text, select the single best model type from the allowed options and normalize the title.\nRespond ONLY with the structured fields required.\n\nAllowed model types are: {ModelType.formatted_options()}\nDetails by type:{ModelType.instruction_listing()}\n"


# ---------- Wikipedia Agent ----------
class WikipediaOutput(BaseModel):
    summary: str = Field(description="Concise Wikipedia-style summary for the topic provided")


WIKIPEDIA_AGENT_PROMPT = "You are a research assistant that fetches and condenses Wikipedia information into a brief,\nbalanced summary focusing on facts likely relevant for downstream analysis."


# ---------- Domain Specialists ----------
def _specialist_instructions(role_key: str, domain: str) -> str:
    """Return tailored role instructions with a brief personalized background.

    role_key must be one of: "History", "Research", "Critic", "Summary", "Business".
    """
    base_len = "Write 120–180 words in a single compact paragraph; avoid bullet lists and fluff."

    if role_key == "History":
        return (
            "You are Dr. Ava Morgan, a cultural historian focused on "
            f"{domain}, with 20 years at the British Film Institute advising on genre timelines.\n"
            "Task: Outline the historical context that matters for accurately framing this work: key genre origins, "
            "movements, technological shifts, regulatory events, and industry milestones that shaped audience expectations.\n"
            "Emphasize time periods, turning points, and why they are directly relevant to this title; avoid plot recap.\n"
            f"{base_len}"
        )

    if role_key == "Research":
        return (
            "You are Casey Lin, an OSINT researcher and media librarian who builds source packs for greenlight reviews in "
            f"{domain}.\n"
            "Task: Describe the concrete sources and metadata you would collect for rigorous analysis: primary sources (official sites, press kits), "
            "databases (e.g., credits, awards, ratings), audience signals (social, forums), and distribution/rights info.\n"
            "List what to verify (names, dates, networks/platforms/studios, territories, certifications) and common pitfalls to avoid.\n"
            "Do not invent facts—focus on the research plan and provenance considerations.\n"
            f"{base_len}"
        )

    if role_key == "Critic":
        return (
            "You are Malik Ortega, a senior critic and craft analyst covering "
            f"{domain} for a decade across major publications.\n"
            "Task: Provide a balanced craft appraisal that could guide an executive: strengths and weaknesses across writing/design, "
            "direction/gameplay, performance/voice, pacing, aesthetics/UX, originality, and audience fit.\n"
            "Offer 1–2 tasteful comps (similar works) and articulate what kind of audience will appreciate this and why.\n"
            "Avoid spoilers and avoid repeating summary/history.\n"
            f"{base_len}"
        )

    if role_key == "Summary":
        return f"You are Priya Shah, an executive brief writer who prepares board-level one-pagers on {domain}.\nTask: Produce a crisp executive synopsis suitable for a decision-maker: premise (one sentence), tonal identity, standout elements (hook/craft), and market positioning (who it serves and why now).\nAssume the reader has no prior context; be clear and non-marketing in tone.\n{base_len}"

    if role_key == "Business":
        return (
            "You are Jordan Reyes, an entertainment strategist and former studio planner working across "
            f"{domain}.\n"
            "Task: Assess commercial framing: likely target segments, distribution patterns (platforms/territories/windows), "
            "monetization levers, brand/IP extension potential, and key risks.\n"
            "Call out the 2–3 leading KPIs an exec should watch (e.g., retention, attach rate, ARPU, awards traction) and why.\n"
            "Keep it analytical and avoid hype; do not repeat plot or craft notes.\n"
            f"{base_len}"
        )

    # Fallback (should not be used)
    return f"You are a seasoned {role_key.lower()} specializing in {domain}.\nProvide a focused note that directly helps a formatting agent produce a professional dossier. {base_len}"


def _domain_for_model(model_type: ModelType) -> str:
    if "game" in model_type.value:
        return "video games"
    if "movie" in model_type.value:
        return "feature films"
    return "television shows"


# ---------- Formatting Agent ----------
def _compose_final_instructions(
    input_model: Type[T],
    additional_info: Sequence[str] | None,
    wikipedia_summary: str,
    specialist_notes: dict[str, str],
) -> str:
    base = input_model.get_instructions(additional_info)
    extras = [
        "Context Pack:",
        f"- Wikipedia: {wikipedia_summary}" if wikipedia_summary else None,
        *(f"- {k}: {v}" for k, v in specialist_notes.items() if v),
    ]
    extra_text = "\n".join(filter(None, extras))
    return f"{base}\n\n{extra_text}" if extra_text else base


# ---------- Orchestration ----------
def run_agents_parsed(input_text: str, console: Console) -> Optional[T]:
    """Orchestrate multiple agents to produce a structured model output.

    Steps:
      1) Detect model type and normalized name
      2) Fetch Wikipedia summary via a dedicated agent
      3) Run domain specialists (history, researcher, critic, summarizer, business)
      4) Run the formatting agent to produce the final structured model

    Returns the parsed model instance or None.
    """

    if Agent is None:  # pragma: no cover - tests patch Agent
        console.print("[red]Pydantic AI is not installed. Install `pydantic-ai` to run this helper.[/red]")
        return None

    provider_model = _provider_model_name()

    # Progress across pipeline: detect -> validate -> wikipedia -> 5 specialists -> format -> render
    total_steps = 1 + 1 + 1 + 5 + 1 + 1
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Detecting model type", total=total_steps)

        # 1) Detection
        detection_agent = Agent(provider_model, output_type=DetectionOutput, instructions=_detection_instructions())
        det = detection_agent.run_sync(input_text)
        det_out = cast(DetectionOutput, det.output)
        progress.update(task, description="Validating model type", advance=1)

        # Validate and build ModelTypeInput
        mt_key = det_out.model_type.strip().lower()
        model_cls_map = ModelType.registry()
        if mt_key not in model_cls_map:
            console.print(f"[red]Unknown detected model type: {mt_key!r}[/red]")
            return None

        model_type = ModelType(mt_key)
        model_type_input = ModelTypeInput(
            model_type=model_type,
            description=det_out.description.strip(),
            formatted_name=det_out.formatted_name.strip(),
            additional_info=det_out.additional_info or None,
        )

        # 2) Wikipedia
        progress.update(task, description="Fetching Wikipedia summary", advance=1)
        wikipedia_agent = Agent(provider_model, output_type=WikipediaOutput, instructions=WIKIPEDIA_AGENT_PROMPT)
        wiki_prompt = f"Title: {model_type_input.formatted_name}\nShort description: {model_type_input.description}"
        wiki = wikipedia_agent.run_sync(wiki_prompt)
        wikipedia_summary = cast(WikipediaOutput, wiki.output).summary

        # 3) Domain specialists (5 sequential)
        domain = _domain_for_model(model_type)
        roles = {
            "History": _specialist_instructions("History", domain),
            "Research": _specialist_instructions("Research", domain),
            "Critic": _specialist_instructions("Critic", domain),
            "Summary": _specialist_instructions("Summary", domain),
            "Business": _specialist_instructions("Business", domain),
        }
        notes: dict[str, str] = {}
        for key, instr in roles.items():
            progress.update(task, description=f"{key} note", advance=1)
            agent = Agent(provider_model, output_type=str, instructions=instr)
            r = agent.run_sync(f"Work: {model_type_input.formatted_name}\nContext: {model_type_input.description}\nIf useful, consider year/platform in: {model_type_input.additional_info}")
            notes[key] = cast(str, r.output)

        # 4) Formatting agent
        progress.update(task, description="Formatting structured model", advance=1)
        input_model: Type[T] = cast(Type[T], model_type_input.model_type.get_model_from_name())
        final_instructions = _compose_final_instructions(
            input_model=input_model,
            additional_info=model_type_input.additional_info,
            wikipedia_summary=wikipedia_summary,
            specialist_notes=notes,
        )
        formatting_agent = Agent(provider_model, output_type=input_model, instructions=final_instructions)
        prompt = input_model.get_user_prompt(model_type_input.formatted_name)
        try:
            result = formatting_agent.run_sync(prompt)
        except Exception as e:  # pragma: no cover - defensive
            console.print(f"[red]Formatting agent failed: {e}[/red]")
            return None

        item_info: Optional[T] = cast(Optional[T], getattr(result, "output", None))
        if item_info is None:
            console.print(f"[red]Failed to parse info for '{model_type_input.formatted_name}'[/red]")
            return None

        # Attach the Wikipedia summary for parity and render
        progress.update(task, description="Rendering output", advance=1)
        setattr(item_info, "wikipedia_summary", wikipedia_summary)
        console.rule(f"[bold cyan]{model_type_input.formatted_name}")
        item_info.render(console)
        console.print("\n")

        return item_info
