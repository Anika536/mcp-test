"""
Unit tests for MCP Test Server
"""

import pytest
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


@pytest.fixture
async def mcp_session():
    """Fixture to create an MCP session."""
    server_params = StdioServerParameters(
        command="mcp-test-server",
        args=[],
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            yield session


@pytest.mark.asyncio
async def test_tool_discovery(mcp_session):
    """Test that all expected tools are discovered."""
    response = await mcp_session.list_tools()
    tool_names = {tool.name for tool in response.tools}
    
    expected_tools = {
        "echo", "add_numbers", "format_json",
        "list_operations", "complex_schema", "timestamp"
    }
    
    assert tool_names == expected_tools


@pytest.mark.asyncio
async def test_echo_tool(mcp_session):
    """Test the echo tool."""
    result = await mcp_session.call_tool("echo", {"message": "test"})
    assert len(result.content) > 0
    assert "test" in result.content[0].text


@pytest.mark.asyncio
async def test_add_numbers_tool(mcp_session):
    """Test the add_numbers tool."""
    result = await mcp_session.call_tool("add_numbers", {"a": 5, "b": 3})
    assert len(result.content) > 0
    assert "8" in result.content[0].text


@pytest.mark.asyncio
async def test_resource_discovery(mcp_session):
    """Test that all expected resources are discovered."""
    response = await mcp_session.list_resources()
    resource_uris = {resource.uri for resource in response.resources}
    
    expected_resources = {
        "mcp://test/static-text",
        "mcp://test/json-data",
        "mcp://test/markdown-doc",
        "mcp://test/config"
    }
    
    assert resource_uris == expected_resources


@pytest.mark.asyncio
async def test_resource_reading(mcp_session):
    """Test reading a resource."""
    result = await mcp_session.read_resource("mcp://test/static-text")
    assert len(result.contents) > 0
    assert len(result.contents[0].text) > 0


@pytest.mark.asyncio
async def test_prompt_discovery(mcp_session):
    """Test that all expected prompts are discovered."""
    response = await mcp_session.list_prompts()
    prompt_names = {prompt.name for prompt in response.prompts}
    
    expected_prompts = {"test-prompt", "debug-prompt"}
    
    assert prompt_names == expected_prompts


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
