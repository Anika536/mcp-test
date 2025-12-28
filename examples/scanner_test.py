"""
MCP Scanner Test Script
=======================
Automated testing script for validating MCP scanner functionality.
Use this to verify that a scanner correctly discovers and parses all server capabilities.
"""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class ScannerTest:
    """Test harness for MCP scanner validation."""
    
    def __init__(self):
        self.results = {
            "tools": {"expected": 6, "found": 0, "passed": False, "details": []},
            "resources": {"expected": 4, "found": 0, "passed": False, "details": []},
            "prompts": {"expected": 2, "found": 0, "passed": False, "details": []},
            "tool_schemas": {"passed": False, "issues": []},
            "resource_reading": {"passed": False, "issues": []},
        }
    
    async def run_all_tests(self):
        """Run complete test suite."""
        server_params = StdioServerParameters(
            command="mcp-test-server",
            args=[],
        )
        
        print("🔍 Starting MCP Scanner Tests...\n")
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                await self.test_tool_discovery(session)
                await self.test_resource_discovery(session)
                await self.test_prompt_discovery(session)
                await self.test_tool_schemas(session)
                await self.test_resource_reading(session)
        
        self.print_results()
        return self.all_tests_passed()
    
    async def test_tool_discovery(self, session):
        """Test that all tools are discovered."""
        print("📋 Test 1: Tool Discovery")
        
        expected_tools = {
            "echo", "add_numbers", "format_json", 
            "list_operations", "complex_schema", "timestamp"
        }
        
        tools_response = await session.list_tools()
        tools = tools_response.tools
        found_tools = {tool.name for tool in tools}
        
        self.results["tools"]["found"] = len(found_tools)
        self.results["tools"]["details"] = list(found_tools)
        self.results["tools"]["passed"] = found_tools == expected_tools
        
        if self.results["tools"]["passed"]:
            print("  ✅ All tools discovered correctly")
        else:
            missing = expected_tools - found_tools
            extra = found_tools - expected_tools
            if missing:
                print(f"  ❌ Missing tools: {missing}")
            if extra:
                print(f"  ⚠️  Extra tools: {extra}")
        print()
    
    async def test_resource_discovery(self, session):
        """Test that all resources are discovered."""
        print("📦 Test 2: Resource Discovery")
        
        expected_resources = {
            "mcp://test/static-text",
            "mcp://test/json-data",
            "mcp://test/markdown-doc",
            "mcp://test/config"
        }
        
        resources_response = await session.list_resources()
        resources = resources_response.resources
        found_resources = {resource.uri for resource in resources}
        
        self.results["resources"]["found"] = len(found_resources)
        self.results["resources"]["details"] = list(found_resources)
        self.results["resources"]["passed"] = found_resources == expected_resources
        
        if self.results["resources"]["passed"]:
            print("  ✅ All resources discovered correctly")
        else:
            missing = expected_resources - found_resources
            extra = found_resources - expected_resources
            if missing:
                print(f"  ❌ Missing resources: {missing}")
            if extra:
                print(f"  ⚠️  Extra resources: {extra}")
        print()
    
    async def test_prompt_discovery(self, session):
        """Test that all prompts are discovered."""
        print("💬 Test 3: Prompt Discovery")
        
        expected_prompts = {"test-prompt", "debug-prompt"}
        
        prompts_response = await session.list_prompts()
        prompts = prompts_response.prompts
        found_prompts = {prompt.name for prompt in prompts}
        
        self.results["prompts"]["found"] = len(found_prompts)
        self.results["prompts"]["details"] = list(found_prompts)
        self.results["prompts"]["passed"] = found_prompts == expected_prompts
        
        if self.results["prompts"]["passed"]:
            print("  ✅ All prompts discovered correctly")
        else:
            missing = expected_prompts - found_prompts
            extra = found_prompts - expected_prompts
            if missing:
                print(f"  ❌ Missing prompts: {missing}")
            if extra:
                print(f"  ⚠️  Extra prompts: {extra}")
        print()
    
    async def test_tool_schemas(self, session):
        """Test that tool schemas are parsed correctly."""
        print("🔍 Test 4: Tool Schema Parsing")
        
        tools_response = await session.list_tools()
        tools = tools_response.tools
        
        # Check specific schema requirements
        issues = []
        
        # Check echo tool
        echo_tool = next((t for t in tools if t.name == "echo"), None)
        if echo_tool:
            if "message" not in echo_tool.inputSchema.get("properties", {}):
                issues.append("echo: missing 'message' property")
            if "message" not in echo_tool.inputSchema.get("required", []):
                issues.append("echo: 'message' should be required")
        else:
            issues.append("echo tool not found")
        
        # Check complex_schema tool
        complex_tool = next((t for t in tools if t.name == "complex_schema"), None)
        if complex_tool:
            props = complex_tool.inputSchema.get("properties", {})
            if "user" not in props:
                issues.append("complex_schema: missing 'user' property")
            elif "properties" not in props.get("user", {}):
                issues.append("complex_schema: 'user' should be nested object")
        else:
            issues.append("complex_schema tool not found")
        
        # Check list_operations enum
        list_tool = next((t for t in tools if t.name == "list_operations"), None)
        if list_tool:
            props = list_tool.inputSchema.get("properties", {})
            if "operation" in props:
                if "enum" not in props["operation"]:
                    issues.append("list_operations: 'operation' should have enum constraint")
        else:
            issues.append("list_operations tool not found")
        
        self.results["tool_schemas"]["issues"] = issues
        self.results["tool_schemas"]["passed"] = len(issues) == 0
        
        if self.results["tool_schemas"]["passed"]:
            print("  ✅ Tool schemas parsed correctly")
        else:
            print(f"  ❌ Schema issues found:")
            for issue in issues:
                print(f"     - {issue}")
        print()
    
    async def test_resource_reading(self, session):
        """Test that resources can be read."""
        print("📖 Test 5: Resource Reading")
        
        issues = []
        
        # Test reading each resource
        test_uris = [
            "mcp://test/static-text",
            "mcp://test/json-data",
            "mcp://test/markdown-doc",
            "mcp://test/config"
        ]
        
        for uri in test_uris:
            try:
                result = await session.read_resource(uri)
                if not result.contents or len(result.contents) == 0:
                    issues.append(f"{uri}: No content returned")
                elif uri == "mcp://test/json-data":
                    # Verify it's valid JSON
                    try:
                        content = result.contents[0].text
                        json.loads(content)
                    except json.JSONDecodeError:
                        issues.append(f"{uri}: Invalid JSON content")
            except Exception as e:
                issues.append(f"{uri}: Error reading - {str(e)}")
        
        self.results["resource_reading"]["issues"] = issues
        self.results["resource_reading"]["passed"] = len(issues) == 0
        
        if self.results["resource_reading"]["passed"]:
            print("  ✅ All resources readable")
        else:
            print(f"  ❌ Resource reading issues:")
            for issue in issues:
                print(f"     - {issue}")
        print()
    
    def print_results(self):
        """Print test results summary."""
        print("=" * 60)
        print("TEST RESULTS SUMMARY")
        print("=" * 60)
        
        total_tests = 5
        passed_tests = sum([
            self.results["tools"]["passed"],
            self.results["resources"]["passed"],
            self.results["prompts"]["passed"],
            self.results["tool_schemas"]["passed"],
            self.results["resource_reading"]["passed"]
        ])
        
        print(f"\nTests Passed: {passed_tests}/{total_tests}\n")
        
        print(f"1. Tool Discovery: {'✅ PASS' if self.results['tools']['passed'] else '❌ FAIL'}")
        print(f"   Expected: {self.results['tools']['expected']}, Found: {self.results['tools']['found']}")
        
        print(f"\n2. Resource Discovery: {'✅ PASS' if self.results['resources']['passed'] else '❌ FAIL'}")
        print(f"   Expected: {self.results['resources']['expected']}, Found: {self.results['resources']['found']}")
        
        print(f"\n3. Prompt Discovery: {'✅ PASS' if self.results['prompts']['passed'] else '❌ FAIL'}")
        print(f"   Expected: {self.results['prompts']['expected']}, Found: {self.results['prompts']['found']}")
        
        print(f"\n4. Tool Schema Parsing: {'✅ PASS' if self.results['tool_schemas']['passed'] else '❌ FAIL'}")
        if self.results['tool_schemas']['issues']:
            print(f"   Issues: {len(self.results['tool_schemas']['issues'])}")
        
        print(f"\n5. Resource Reading: {'✅ PASS' if self.results['resource_reading']['passed'] else '❌ FAIL'}")
        if self.results['resource_reading']['issues']:
            print(f"   Issues: {len(self.results['resource_reading']['issues'])}")
        
        print("\n" + "=" * 60)
        
        # Export results to JSON
        with open("scanner_test_results.json", "w") as f:
            json.dump(self.results, f, indent=2)
        print("📄 Detailed results saved to: scanner_test_results.json")
    
    def all_tests_passed(self):
        """Check if all tests passed."""
        return all([
            self.results["tools"]["passed"],
            self.results["resources"]["passed"],
            self.results["prompts"]["passed"],
            self.results["tool_schemas"]["passed"],
            self.results["resource_reading"]["passed"]
        ])


async def main():
    """Run scanner tests."""
    tester = ScannerTest()
    success = await tester.run_all_tests()
    
    if success:
        print("\n🎉 All scanner tests passed!")
        return 0
    else:
        print("\n⚠️  Some scanner tests failed. Review results above.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
