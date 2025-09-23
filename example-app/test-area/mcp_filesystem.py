"""
MCP FileSystem Module

This module provides file system operations through the Model Context Protocol (MCP).
It connects to an MCP filesystem server to perform file operations.
"""

import asyncio
import subprocess
import json
from typing import List, Dict, Any, Optional


class MCPFileSystem:
    """MCP FileSystem client for file operations."""

    def __init__(self, server_command: str = "filesystem-operations-mcp", server_args: Optional[List[str]] = None):
        """Initialize MCP FileSystem client.

        Args:
            server_command: Command to start the MCP filesystem server
            server_args: Arguments for the server command
        """
        self.server_command = server_command
        self.server_args = server_args or []

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

    async def list_directory(self, path: str) -> List[Dict[str, Any]]:
        """List contents of a directory.

        Args:
            path: Directory path to list

        Returns:
            List of file/directory information
        """
        try:
            result = await self._call_tool("list_dir", {"path": path})
            if result and 'content' in result:
                return result['content']
            return []
        except Exception as e:
            print(f"Error listing directory {path}: {e}")
            return []

    async def read_file(self, path: str) -> str:
        """Read contents of a file.

        Args:
            path: File path to read

        Returns:
            File contents as string
        """
        try:
            result = await self._call_tool("read_file", {"path": path})
            if result and 'content' in result:
                return result['content']
            return ""
        except Exception as e:
            print(f"Error reading file {path}: {e}")
            return ""

    async def write_file(self, path: str, content: str) -> bool:
        """Write content to a file.

        Args:
            path: File path to write
            content: Content to write

        Returns:
            True if successful, False otherwise
        """
        try:
            result = await self._call_tool("write_file", {"path": path, "content": content})
            return result is not None
        except Exception as e:
            print(f"Error writing file {path}: {e}")
            return False

    async def create_directory(self, path: str) -> bool:
        """Create a new directory.

        Args:
            path: Directory path to create

        Returns:
            True if successful, False otherwise
        """
        try:
            result = await self._call_tool("create_dir", {"path": path})
            return result is not None
        except Exception as e:
            print(f"Error creating directory {path}: {e}")
            return False


# Convenience functions for easy use
async def list_dir(path: str) -> List[Dict[str, Any]]:
    """List directory contents."""
    fs = MCPFileSystem()
    return await fs.list_directory(path)

async def read_file(path: str) -> str:
    """Read file contents."""
    fs = MCPFileSystem()
    return await fs.read_file(path)

async def write_file(path: str, content: str) -> bool:
    """Write content to file."""
    fs = MCPFileSystem()
    return await fs.write_file(path, content)

async def create_dir(path: str) -> bool:
    """Create directory."""
    fs = MCPFileSystem()
    return await fs.create_directory(path)


if __name__ == "__main__":
    # Example usage
    async def main():
        print("Testing MCP FileSystem...")

        # List current directory
        print("Listing current directory:")
        files = await list_dir(".")
        if files:
            for file_info in files:
                print(f"  {file_info}")
        else:
            print("  No files found or error occurred")

        # Try to read this file
        print(f"\nReading {__file__}:")
        content = await read_file(__file__)
        if content:
            print(content[:200] + "...")
        else:
            print("  Could not read file")

    asyncio.run(main())
