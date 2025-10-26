"""Comprehensive tests for wikipedia_tool module."""

from unittest.mock import patch

from aiss.models.shared import ModelTypeResult
from aiss.openai_direct.wikipedia_tool import (
    augment_instructions_with_tool_hint,
    augment_prompt_with_wikipedia_context,
    build_wikipedia_topic_context,
)


class MockModelFormat:
    """Mock model format for testing."""

    model_name = "TestModel"
    key_trait = "test_trait"
    description = "Test Description"


class TestBuildWikipediaTopicContext:
    """Test build_wikipedia_topic_context function."""

    @patch("aiss.openai_direct.wikipedia_tool.summary")
    def test_build_context_with_all_attributes(self, mock_summary):
        """Test building context with all model attributes present."""
        mock_summary.return_value = "Mock Wikipedia summary about the topic."

        model_type_result = ModelTypeResult(
            model_type="movie",
            description="Test movie description",
            formatted_name="Test Movie",
            additional_info=["2020", "Drama"],
        )

        result = build_wikipedia_topic_context(MockModelFormat, model_type_result)

        assert result is not None
        assert len(result) == 2
        wikipedia_summary, context = result
        assert "Mock Wikipedia summary" in wikipedia_summary
        assert "Test Movie" in context
        assert "TestModel" in context
        assert "test_trait" in context
        mock_summary.assert_called_once_with("Test Movie: Test movie description", sentences=10)

    @patch("aiss.openai_direct.wikipedia_tool.summary")
    def test_build_context_without_key_trait(self, mock_summary):
        """Test building context when key_trait is missing."""
        mock_summary.return_value = "Wikipedia content"

        class MinimalModelFormat:
            model_name = "Minimal"

        model_type_result = ModelTypeResult(
            model_type="test",
            description="Test title description",
            formatted_name="Test Title",
            additional_info=[],
        )

        result = build_wikipedia_topic_context(MinimalModelFormat, model_type_result)

        assert result is not None
        wikipedia_summary, context = result
        assert "Wikipedia content" in wikipedia_summary
        assert "Test Title" in context
        assert "Minimal" in context

    @patch("aiss.openai_direct.wikipedia_tool.summary")
    def test_build_context_without_description(self, mock_summary):
        """Test building context when description is missing."""
        mock_summary.return_value = "Wiki summary"

        class NoDescriptionFormat:
            model_name = "NoDesc"
            key_trait = "trait"

        model_type_result = ModelTypeResult(
            model_type="test",
            description="Another title description",
            formatted_name="Another Title",
        )

        result = build_wikipedia_topic_context(NoDescriptionFormat, model_type_result)

        assert result is not None
        wikipedia_summary, context = result
        assert "Wiki summary" in wikipedia_summary
        assert "Another Title" in context

    @patch("aiss.openai_direct.wikipedia_tool.summary")
    def test_build_context_with_additional_info(self, mock_summary):
        """Test building context with additional info."""
        mock_summary.return_value = "Summary with additional info"

        model_type_result = ModelTypeResult(
            model_type="complex",
            description="Complex title with additional information",
            formatted_name="Complex Title",
            additional_info=["Info1", "Info2", "Info3"],
        )

        result = build_wikipedia_topic_context(MockModelFormat, model_type_result)

        assert result is not None
        wikipedia_summary, context = result
        assert "Summary with additional info" in wikipedia_summary
        assert "Complex Title" in context
        assert "Additional Info" in context

    def test_build_context_empty_formatted_name(self):
        """Test building context with empty formatted name returns empty string."""
        model_type_result = ModelTypeResult(
            model_type="test",
            description="Empty test",
            formatted_name="",
        )

        result = build_wikipedia_topic_context(MockModelFormat, model_type_result)

        assert result == ""

    def test_build_context_whitespace_formatted_name(self):
        """Test building context with whitespace-only formatted name."""
        model_type_result = ModelTypeResult(
            model_type="test",
            description="Whitespace test",
            formatted_name="   ",
        )

        result = build_wikipedia_topic_context(MockModelFormat, model_type_result)

        assert result == ""

    @patch("aiss.openai_direct.wikipedia_tool.summary")
    def test_build_context_wikipedia_exception(self, mock_summary, capsys):
        """Test handling Wikipedia API exception."""
        mock_summary.side_effect = Exception("Wikipedia API Error")

        model_type_result = ModelTypeResult(
            model_type="test",
            description="Nonexistent article test",
            formatted_name="Nonexistent Article",
        )

        result = build_wikipedia_topic_context(MockModelFormat, model_type_result)

        # Function returns None on exception (no return statement in except block)
        assert result is None

        # Check error was printed
        captured = capsys.readouterr()
        assert "Error fetching Wikipedia summary" in captured.out
        assert "Wikipedia API Error" in captured.out

    @patch("aiss.openai_direct.wikipedia_tool.summary")
    def test_build_context_with_none_additional_info(self, mock_summary):
        """Test building context when additional_info is None."""
        mock_summary.return_value = "Summary text"

        model_type_result = ModelTypeResult(
            model_type="test",
            description="Test description",
            formatted_name="Test",
            additional_info=None,
        )

        result = build_wikipedia_topic_context(MockModelFormat, model_type_result)

        assert result is not None
        wikipedia_summary, context = result
        assert "Summary text" in wikipedia_summary

    @patch("aiss.openai_direct.wikipedia_tool.summary")
    def test_build_context_without_model_name_attribute(self, mock_summary):
        """Test building context when model_name attribute is missing."""
        mock_summary.return_value = "Wiki content"

        class NoModelName:
            pass

        model_type_result = ModelTypeResult(
            model_type="test",
            description="Title description",
            formatted_name="Title",
        )

        result = build_wikipedia_topic_context(NoModelName, model_type_result)

        assert result is not None
        wikipedia_summary, context = result
        # Should use class name as fallback
        assert "NoModelName" in context


class TestAugmentPromptWithWikipediaContext:
    """Test augment_prompt_with_wikipedia_context function."""

    def test_augment_prompt_with_context(self):
        """Test augmenting prompt with Wikipedia context."""
        base_prompt = "Tell me about this movie."
        wikipedia_summary = "This is a Wikipedia summary."
        context = "Title: Test Movie, Format: Drama"

        result = augment_prompt_with_wikipedia_context(base_prompt, wikipedia_summary, context)

        assert base_prompt in result
        assert wikipedia_summary in result
        assert context in result
        assert "Topic & Context Hint:" in result
        assert "Wikipedia Summary:" in result

    def test_augment_prompt_with_empty_context(self):
        """Test augmenting prompt with empty context returns base prompt."""
        base_prompt = "Original prompt"
        wikipedia_summary = "Summary"
        context = ""

        result = augment_prompt_with_wikipedia_context(base_prompt, wikipedia_summary, context)

        assert result == base_prompt
        assert wikipedia_summary not in result
        assert "Topic & Context Hint:" not in result

    def test_augment_prompt_with_none_context(self):
        """Test augmenting prompt with None context."""
        base_prompt = "Original prompt"
        wikipedia_summary = "Summary"
        context = None

        result = augment_prompt_with_wikipedia_context(base_prompt, wikipedia_summary, context)

        # Should treat None as falsy and return base prompt
        assert result == base_prompt

    def test_augment_prompt_multiline_base(self):
        """Test augmenting multiline base prompt."""
        base_prompt = "Line 1\nLine 2\nLine 3"
        wikipedia_summary = "Wiki summary"
        context = "Context info"

        result = augment_prompt_with_wikipedia_context(base_prompt, wikipedia_summary, context)

        assert base_prompt in result
        assert "Topic & Context Hint:" in result
        assert context in result

    def test_augment_prompt_special_characters(self):
        """Test augmenting prompt with special characters."""
        base_prompt = "Tell me about: <movie>?"
        wikipedia_summary = "Summary with 'quotes' and \"double quotes\""
        context = "Context: Test & More"

        result = augment_prompt_with_wikipedia_context(base_prompt, wikipedia_summary, context)

        assert base_prompt in result
        assert wikipedia_summary in result
        assert context in result


class TestAugmentInstructionsWithToolHint:
    """Test augment_instructions_with_tool_hint function."""

    def test_augment_instructions_with_context(self):
        """Test augmenting instructions with tool hint."""
        instructions = "You are a helpful assistant."
        wikipedia_summary = "Wikipedia summary content."
        context = "Title: Movie, Year: 2020"

        result = augment_instructions_with_tool_hint(instructions, wikipedia_summary, context)

        assert instructions in result
        assert wikipedia_summary in result
        assert context in result
        assert "Prefer the following context:" in result
        assert "Wikipedia Summary:" in result

    def test_augment_instructions_with_empty_context(self):
        """Test augmenting instructions with empty context returns original."""
        instructions = "System instructions"
        wikipedia_summary = "Summary"
        context = ""

        result = augment_instructions_with_tool_hint(instructions, wikipedia_summary, context)

        assert result == instructions
        assert wikipedia_summary not in result
        assert "Prefer the following context:" not in result

    def test_augment_instructions_with_none_context(self):
        """Test augmenting instructions with None context."""
        instructions = "System instructions"
        wikipedia_summary = "Summary"
        context = None

        result = augment_instructions_with_tool_hint(instructions, wikipedia_summary, context)

        # Should treat None as falsy and return original instructions
        assert result == instructions

    def test_augment_instructions_complex_context(self):
        """Test augmenting instructions with complex context."""
        instructions = "Analyze the following work."
        wikipedia_summary = "Detailed Wikipedia article about the subject."
        context = "Title: Complex Work, Format: Drama, Key Trait: Character Development, Additional Info: 2020; Award Winner"

        result = augment_instructions_with_tool_hint(instructions, wikipedia_summary, context)

        assert instructions in result
        assert context in result
        assert "Character Development" in result
        assert "Award Winner" in result

    def test_augment_instructions_multiline(self):
        """Test augmenting multiline instructions."""
        instructions = "Rule 1: Be accurate\nRule 2: Be helpful\nRule 3: Be concise"
        wikipedia_summary = "Summary"
        context = "Context data"

        result = augment_instructions_with_tool_hint(instructions, wikipedia_summary, context)

        assert "Rule 1" in result
        assert "Rule 2" in result
        assert "Rule 3" in result
        assert context in result

    def test_augment_instructions_empty_summary(self):
        """Test augmenting instructions with empty Wikipedia summary."""
        instructions = "System prompt"
        wikipedia_summary = ""
        context = "Valid context"

        result = augment_instructions_with_tool_hint(instructions, wikipedia_summary, context)

        # Should still augment even with empty summary
        assert instructions in result
        assert context in result
        assert "Prefer the following context:" in result

    def test_augment_instructions_preserves_formatting(self):
        """Test that augmentation preserves original instruction formatting."""
        instructions = "  Indented instructions  "
        wikipedia_summary = "Summary"
        context = "Context"

        result = augment_instructions_with_tool_hint(instructions, wikipedia_summary, context)

        assert instructions in result  # Original spacing preserved


class TestIntegration:
    """Integration tests combining multiple functions."""

    @patch("aiss.openai_direct.wikipedia_tool.summary")
    def test_full_workflow(self, mock_summary):
        """Test complete workflow from building context to augmenting prompt."""
        mock_summary.return_value = "Complete Wikipedia article about the topic."

        model_type_result = ModelTypeResult(
            model_type="movie",
            description="Sci-Fi action movie from 1999",
            formatted_name="The Matrix",
            additional_info=["1999", "Sci-Fi"],
        )

        # Build context
        result = build_wikipedia_topic_context(MockModelFormat, model_type_result)
        assert result is not None
        wikipedia_summary, context = result

        # Augment prompt
        base_prompt = "Analyze this movie"
        augmented_prompt = augment_prompt_with_wikipedia_context(base_prompt, wikipedia_summary, context)

        assert "The Matrix" in augmented_prompt
        assert "Complete Wikipedia article" in augmented_prompt
        assert base_prompt in augmented_prompt

        # Augment instructions
        instructions = "You analyze movies."
        augmented_instructions = augment_instructions_with_tool_hint(instructions, wikipedia_summary, context)

        assert "The Matrix" in augmented_instructions
        assert instructions in augmented_instructions

    @patch("aiss.openai_direct.wikipedia_tool.summary")
    def test_workflow_with_minimal_model(self, mock_summary):
        """Test workflow with minimal model configuration."""
        mock_summary.return_value = "Brief summary"

        class MinimalModel:
            pass

        model_type_result = ModelTypeResult(
            model_type="test",
            description="Simple work description",
            formatted_name="Simple Work",
        )

        result = build_wikipedia_topic_context(MinimalModel, model_type_result)
        assert result is not None
        wikipedia_summary, context = result

        augmented = augment_prompt_with_wikipedia_context("Question?", wikipedia_summary, context)
        assert "Question?" in augmented
        assert "Brief summary" in augmented
