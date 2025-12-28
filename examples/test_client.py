"""
MCP Test Client
===============
Example client for testing the MCP test server.
Demonstrates how to connect to the server and use its tools.
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_all_tools():
    """Test all available tools on the MCP server."""
    
    server_params = StdioServerParameters(
        command="mcp-test-server",
        args=[],
    )
    
    print("🚀 Connecting to MCP Test Server...")
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()
            print("✅ Connected successfully!\n")
            
            # List available tools
            print("📋 Listing available tools...")
            tools_response = await session.list_tools()
            tools = tools_response.tools
            print(f"Found {len(tools)} tools:")
            for tool in tools:
                print(f"  - {tool.name}: {tool.description}")
            print()
            
            # Test echo tool
            print("🔧 Testing 'echo' tool...")
            result = await session.call_tool("echo", {"message": "Hello, MCP!"})
            print(f"Result: {result.content[0].text}\n")
            
            # Test add_numbers tool
            print("🔧 Testing 'add_numbers' tool...")
            result = await session.call_tool("add_numbers", {"a": 42, "b": 8})
            print(f"Result: {result.content[0].text}\n")
            
            # Test format_json tool
            print("🔧 Testing 'format_json' tool...")
            test_data = {"name": "Test", "values": [1, 2, 3], "active": True}
            result = await session.call_tool("format_json", {"data": test_data, "indent": 2})
            print(f"Result:\n{result.content[0].text}\n")
            
            # Test list_operations tool
            print("🔧 Testing 'list_operations' tool...")
            result = await session.call_tool(
                "list_operations", 
                {"items": ["zebra", "apple", "mango", "banana"], "operation": "sort"}
            )
            print(f"Result: {result.content[0].text}\n")
            
            # Test timestamp tool
            print("🔧 Testing 'timestamp' tool...")
            result = await session.call_tool("timestamp", {"format": "readable"})
            print(f"Result: {result.content[0].text}\n")
            
            # List resources
            print("📦 Listing available resources...")
            resources_response = await session.list_resources()
            resources = resources_response.resources
            print(f"Found {len(resources)} resources:")
            for resource in resources:
                print(f"  - {resource.name} ({resource.uri})")
            print()
            
            # Read a resource
            print("📖 Reading 'static-text' resource...")
            resource_content = await session.read_resource("mcp://test/static-text")
            print(f"Content:\n{resource_content.contents[0].text}\n")
            
            # List prompts
            print("💬 Listing available prompts...")
            prompts_response = await session.list_prompts()
            prompts = prompts_response.prompts
            print(f"Found {len(prompts)} prompts:")
            for prompt in prompts:
                print(f"  - {prompt.name}: {prompt.description}")
            print()
            
            print("✨ All tests completed successfully!")


async def test_complex_schema():
    """Test the complex schema tool specifically."""
    
    server_params = StdioServerParameters(
        command="mcp-test-server",
        args=[],
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("🔧 Testing complex schema tool...")
            
            complex_input = {
                "user": {
                    "name": "Jane Doe",
                    "age": 30,
                    "tags": ["developer", "python", "mcp"],
                    "metadata": {
                        "department": "Engineering",
                        "level": "Senior",
                        "location": "Remote"
                    }
                },
                "options": {
                    "verbose": True,
                    "format": "json"
                }
            }
            
            result = await session.call_tool("complex_schema", complex_input)
            print(f"Result:\n{result.content[0].text}")


if __name__ == "__main__":
    print("=" * 60)
    print("MCP Test Client - Tool Testing")
    print("=" * 60)
    print()
    
    try:
        asyncio.run(test_all_tools())
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("Complex Schema Test")
    print("=" * 60)
    print()
    
    try:
        asyncio.run(test_complex_schema())
    except Exception as e:
        print(f"❌ Error: {e}")
