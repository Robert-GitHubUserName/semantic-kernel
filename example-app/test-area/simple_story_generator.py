#!/usr/bin/env python3
"""
Simple Semantic Kernel + Ollama Sample

This script demonstrates using Semantic Kernel with Ollama to generate
a sci-fi story and save it to a file.
"""

import asyncio
import os
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import KernelArguments
import openai


class SimpleStoryGenerator:
    """Simple story generator using Semantic Kernel and Ollama."""

    def __init__(self):
        """Initialize the story generator."""
        self.kernel = Kernel()

        # Configure Ollama as the AI service using OpenAI client with custom base URL
        ollama_client = openai.AsyncOpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama"  # Dummy key for Ollama
        )

        self.service = OpenAIChatCompletion(
            ai_model_id="gemma3:latest",
            service_id="ollama-gemma3",
            async_client=ollama_client
        )

        self.kernel.add_service(self.service)

        # Register the story generation function
        self.kernel.add_function(
            plugin_name="story_writer",
            function_name="write_sci_fi_story",
            prompt="""
            Write a short, engaging sci-fi story (200-300 words) with the following elements:
            - Futuristic technology
            - Space exploration or alien encounters
            - A compelling plot with a twist
            - Well-developed characters
            - Atmospheric descriptions

            Make it creative and entertaining. Focus on world-building and suspense.

            Story:
            """
        )

    async def generate_story(self) -> str:
        """Generate a sci-fi story."""
        try:
            result = await self.kernel.invoke(
                function_name="write_sci_fi_story",
                plugin_name="story_writer",
                arguments=KernelArguments()
            )
            return str(result)
        except Exception as e:
            return f"Error generating story: {e}"

    def save_to_file(self, content: str, filename: str) -> bool:
        """Save content to a file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Story saved to {filename}")
            return True
        except Exception as e:
            print(f"Error saving to file: {e}")
            return False


async def main():
    """Main function to generate and save a sci-fi story."""
    print("Initializing story generator...")

    # Create the generator
    generator = SimpleStoryGenerator()

    print("Generating sci-fi story...")

    # Generate the story
    story = await generator.generate_story()

    if story.startswith("Error"):
        print(f"Failed to generate story: {story}")
        return

    print("Story generated successfully!")
    print("\n" + "="*50)
    print("GENERATED STORY:")
    print("="*50)
    print(story)
    print("="*50)

    # Save to file
    filename = "sci-fi-01.md"
    success = generator.save_to_file(story, filename)

    if success:
        print(f"\nStory saved to {filename}")
        print(f"File size: {os.path.getsize(filename)} bytes")
    else:
        print("\nFailed to save story to file")


if __name__ == "__main__":
    print("Sci-Fi Story Generator")
    print("Using Semantic Kernel + Ollama (gemma3:latest)")
    print("-" * 50)

    # Run the async main function
    asyncio.run(main())
