"""
MCP Browser Module

This module provides browser automation through the Model Context Protocol (MCP).
It connects to an MCP browser server (Playwright) to perform web automation tasks.
"""

import asyncio
import subprocess
import json
from typing import List, Dict, Any, Optional


class MCPBrowser:
    """MCP Browser client for web automation."""

    def __init__(self, server_command: str = "npx", server_args: Optional[List[str]] = None):
        """Initialize MCP Browser client.

        Args:
            server_command: Command to start the MCP browser server (usually 'npx')
            server_args: Arguments for the server command (usually ['@playwright/mcp@latest'])
        """
        self.server_command = server_command
        self.server_args = server_args or ["@playwright/mcp@latest"]

    async def _call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Call an MCP tool with the given arguments.

        Args:
            tool_name: Name of the tool to call
            arguments: Arguments for the tool

        Returns:
            Tool execution result
        """
        try:
            # Start the MCP server process
            process = await asyncio.create_subprocess_exec(
                self.server_command, *self.server_args,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            # Prepare the MCP request
            request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": arguments
                }
            }

            # Send request
            request_json = json.dumps(request).encode('utf-8')
            process.stdin.write(request_json)
            await process.stdin.drain()
            process.stdin.close()

            # Read response
            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                error_msg = stderr.decode('utf-8') if stderr else "Unknown error"
                raise Exception(f"MCP server error: {error_msg}")

            response = json.loads(stdout.decode('utf-8'))
            if 'error' in response:
                raise Exception(f"MCP error: {response['error']}")

            return response.get('result')

        except Exception as e:
            print(f"Error calling MCP tool {tool_name}: {e}")
            return None

    async def navigate(self, url: str) -> bool:
        """Navigate to a URL.

        Args:
            url: URL to navigate to

        Returns:
            True if successful, False otherwise
        """
        try:
            result = await self._call_tool("browser_navigate", {"url": url})
            return result is not None
        except Exception as e:
            print(f"Error navigating to {url}: {e}")
            return False

    async def click_element(self, selector: str) -> bool:
        """Click on an element by selector.

        Args:
            selector: CSS selector for the element to click

        Returns:
            True if successful, False otherwise
        """
        try:
            result = await self._call_tool("browser_click", {"selector": selector})
            return result is not None
        except Exception as e:
            print(f"Error clicking element {selector}: {e}")
            return False

    async def type_text(self, selector: str, text: str) -> bool:
        """Type text into an element.

        Args:
            selector: CSS selector for the input element
            text: Text to type

        Returns:
            True if successful, False otherwise
        """
        try:
            result = await self._call_tool("browser_type", {"selector": selector, "text": text})
            return result is not None
        except Exception as e:
            print(f"Error typing text into {selector}: {e}")
            return False

    async def get_page_content(self) -> str:
        """Get the current page content.

        Returns:
            Page HTML content
        """
        try:
            result = await self._call_tool("browser_get_content", {})
            if result and 'content' in result:
                return result['content']
            return ""
        except Exception as e:
            print(f"Error getting page content: {e}")
            return ""

    async def take_screenshot(self, filename: str = "screenshot.png") -> bool:
        """Take a screenshot of the current page.

        Args:
            filename: Filename for the screenshot

        Returns:
            True if successful, False otherwise
        """
        try:
            result = await self._call_tool("browser_screenshot", {"filename": filename})
            return result is not None
        except Exception as e:
            print(f"Error taking screenshot: {e}")
            return False

    async def wait_for_element(self, selector: str, timeout: int = 10000) -> bool:
        """Wait for an element to appear.

        Args:
            selector: CSS selector to wait for
            timeout: Timeout in milliseconds

        Returns:
            True if element found, False otherwise
        """
        try:
            result = await self._call_tool("browser_wait_for", {"selector": selector, "timeout": timeout})
            return result is not None
        except Exception as e:
            print(f"Error waiting for element {selector}: {e}")
            return False

    async def get_element_text(self, selector: str) -> str:
        """Get text content of an element.

        Args:
            selector: CSS selector for the element

        Returns:
            Element text content
        """
        try:
            result = await self._call_tool("browser_get_text", {"selector": selector})
            if result and 'text' in result:
                return result['text']
            return ""
        except Exception as e:
            print(f"Error getting text from {selector}: {e}")
            return ""


# Convenience functions for easy use
async def navigate(url: str) -> bool:
    """Navigate to URL."""
    browser = MCPBrowser()
    return await browser.navigate(url)

async def click(selector: str) -> bool:
    """Click element."""
    browser = MCPBrowser()
    return await browser.click_element(selector)

async def type_text(selector: str, text: str) -> bool:
    """Type text into element."""
    browser = MCPBrowser()
    return await browser.type_text(selector, text)

async def get_content() -> str:
    """Get page content."""
    browser = MCPBrowser()
    return await browser.get_page_content()

async def screenshot(filename: str = "screenshot.png") -> bool:
    """Take screenshot."""
    browser = MCPBrowser()
    return await browser.take_screenshot(filename)

async def wait_for(selector: str, timeout: int = 10000) -> bool:
    """Wait for element."""
    browser = MCPBrowser()
    return await browser.wait_for_element(selector, timeout)


if __name__ == "__main__":
    # Example usage
    async def main():
        print("Testing MCP Browser...")

        # Navigate to a test page
        print("Navigating to httpbin.org...")
        success = await navigate("https://httpbin.org/")
        if success:
            print("Navigation successful")

            # Wait a bit for page to load
            await asyncio.sleep(2)

            # Get page content
            print("Getting page content...")
            content = await get_content()
            if content:
                print(f"Page content length: {len(content)}")
                print("First 200 chars:", content[:200])
            else:
                print("Could not get page content")
        else:
            print("Navigation failed")

    asyncio.run(main())
