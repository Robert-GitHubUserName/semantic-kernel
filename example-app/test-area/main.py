"""
Main Application - Semantic Kernel with Ollama Integration

This module integrates Microsoft Semantic Kernel with Ollama for AI-powered
file and browser operations using MCP tools.
"""

import asyncio
import os
from typing import Dict, Any, List
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import KernelFunctionFromPrompt, KernelArguments
import ollama
import openai

# Import our MCP modules
from mcp_filesystem import MCPFileSystem
from mcp_browser import MCPBrowser


class AIAgent:
    """AI Agent powered by Semantic Kernel and Ollama."""

    def __init__(self):
        """Initialize the AI agent with Semantic Kernel and Ollama."""
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

        # Initialize MCP tools
        self.fs_client = MCPFileSystem()
        self.browser_client = MCPBrowser()

        # Register semantic functions
        self._register_functions()

    def _register_functions(self):
        """Register semantic functions for various tasks."""

        # File analysis function
        file_analysis_prompt = """
        Analyze the following file content and provide a summary.
        Include key information about the file's purpose, structure, and any important details.

        File: {{file_path}}
        Content: {{file_content}}

        Summary:
        """

        self.file_analysis_func = self.kernel.add_function(
            plugin_name="file_ops",
            function_name="analyze_file",
            prompt=file_analysis_prompt
        )

        # Code generation function
        code_gen_prompt = """
        Generate Python code based on the following description.
        Make sure the code is well-documented and follows best practices.

        Description: {{description}}

        Generated Code:
        """

        self.code_gen_func = self.kernel.add_function(
            plugin_name="code_gen",
            function_name="generate_code",
            prompt=code_gen_prompt
        )

        # Web automation planning function
        web_automation_prompt = """
        Plan a sequence of web automation steps to accomplish the following task.
        Provide step-by-step instructions that can be executed by a browser automation tool.

        Task: {{task}}

        Steps:
        """

        self.web_automation_func = self.kernel.add_function(
            plugin_name="web_ops",
            function_name="plan_web_automation",
            prompt=web_automation_prompt
        )

    async def analyze_file(self, file_path: str) -> str:
        """Analyze a file using AI.

        Args:
            file_path: Path to the file to analyze

        Returns:
            AI-generated analysis of the file
        """
        try:
            # Read file content using MCP
            content = await self.fs_client.read_file(file_path)

            if not content:
                return f"Could not read file: {file_path}"

            # Use Semantic Kernel for analysis
            args = KernelArguments(file_path=file_path, file_content=content[:2000])
            result = await self.kernel.invoke(
                function_name="analyze_file",
                plugin_name="file_ops",
                arguments=args
            )

            return str(result)

        except Exception as e:
            return f"Error analyzing file: {e}"

    async def generate_code(self, description: str) -> str:
        """Generate code based on description.

        Args:
            description: Description of the code to generate

        Returns:
            Generated code
        """
        try:
            print(f"DEBUG: Attempting to generate code for description: {description}")
            args = KernelArguments(description=description)
            print(f"DEBUG: Created KernelArguments: {args}")
            print(f"DEBUG: Invoking function 'generate_code' in plugin 'code_gen'")
            result = await self.kernel.invoke(
                function_name="generate_code",
                plugin_name="code_gen",
                arguments=args
            )
            print(f"DEBUG: Invoke result: {result}")
            return str(result)
        except Exception as e:
            print(f"DEBUG: Exception occurred: {type(e).__name__}: {e}")
            import traceback
            print(f"DEBUG: Full traceback: {traceback.format_exc()}")
            return f"Error generating code: {e}"

    async def plan_web_task(self, task: str) -> str:
        """Plan web automation steps for a task.

        Args:
            task: Description of the web automation task

        Returns:
            Step-by-step plan for web automation
        """
        try:
            args = KernelArguments(task=task)
            result = await self.kernel.invoke(
                function_name="plan_web_automation",
                plugin_name="web_ops",
                arguments=args
            )
            return str(result)
        except Exception as e:
            return f"Error planning web task: {e}"

    async def execute_web_automation(self, plan: str) -> str:
        """Execute web automation based on a plan.

        Args:
            plan: Step-by-step automation plan

        Returns:
            Results of the automation
        """
        # This is a simplified implementation
        # In a real scenario, you'd parse the plan and execute steps
        try:
            # For now, just navigate to a test site
            success = await self.browser_client.navigate("https://httpbin.org/")
            if success:
                content = await self.browser_client.get_page_content()
                return f"Successfully navigated. Page content length: {len(content)}"
            else:
                return "Failed to navigate"
        except Exception as e:
            return f"Error in web automation: {e}"

    async def test_connection(self) -> str:
        """Test the Ollama connection.

        Returns:
            Test result message
        """
        try:
            # Test direct Ollama connection
            response = ollama.chat(
                model='gemma3:latest',
                messages=[{'role': 'user', 'content': 'Say "Ollama connection successful" in exactly those words.'}]
            )
            return response['message']['content']
        except Exception as e:
            return f"Ollama connection failed: {e}"

    async def test_semantic_kernel(self) -> str:
        """Test Semantic Kernel integration.

        Returns:
            Test result message
        """
        try:
            # Simple test function
            test_func = self.kernel.add_function_from_prompt(
                function_name="test",
                plugin_name="test",
                prompt="You are connected to Semantic Kernel. Say 'Semantic Kernel integration successful'."
            )

            result = await self.kernel.invoke(test_func)
            return str(result)
        except Exception as e:
            return f"Semantic Kernel test failed: {e}"


async def main():
    """Main function for testing the AI agent."""
    print("Initializing AI Agent...")
    agent = AIAgent()

    print("\n1. Testing Ollama connection...")
    ollama_result = await agent.test_connection()
    print(f"Result: {ollama_result}")

    print("\n2. Testing Semantic Kernel...")
    sk_result = await agent.test_semantic_kernel()
    print(f"Result: {sk_result}")

    print("\n3. Testing file analysis...")
    analysis_result = await agent.analyze_file(__file__)
    print(f"Analysis: {analysis_result[:200]}...")

    print("\n4. Testing code generation...")
    code_result = await agent.generate_code("Create a simple Python function to calculate factorial")
    print(f"Generated code: {code_result[:200]}...")

    print("\n5. Testing web automation planning...")
    plan_result = await agent.plan_web_task("Check the current weather in New York")
    print(f"Plan: {plan_result[:200]}...")

    print("\nAI Agent testing complete!")


if __name__ == "__main__":
    asyncio.run(main())
