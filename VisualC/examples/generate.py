import os
import pathlib
import uuid

REPOSITORY_ROOT = pathlib.Path(__file__).parent.parent.parent

def generate(category, example_name):
    guid = str(uuid.uuid4()).upper()
    text = f"""
<?xml version="1.0" encoding="utf-8"?>
<Project DefaultTargets="Build" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <PropertyGroup Label="Globals">
    <ProjectGuid>{{{guid}}}</ProjectGuid>
  </PropertyGroup>
  <Import Project="$(VCTargetsPath)\\Microsoft.Cpp.Default.props" />
  <Import Project="$(VCTargetsPath)\\Microsoft.Cpp.props" />
  <ItemGroup>
    <None Include="$(SolutionDir)\\..\\examples\\{category}\\{example_name}\\README.txt" />
    <ClCompile Include="$(SolutionDir)\\..\\examples\\{category}\\{example_name}\\*.c" />
  </ItemGroup>
  <Import Project="$(VCTargetsPath)\\Microsoft.Cpp.targets" />
</Project>
""".strip()

    project_file = REPOSITORY_ROOT / "VisualC" / "examples" / category / example_name / f"{example_name}.vcxproj"

    if project_file.exists():
        print("Skipping:", project_file)
        return

    print("Generating file:", project_file)
    os.makedirs(project_file.parent, exist_ok=True)
    with open(project_file, "w", encoding="utf-8") as f:
        f.write(text)


def main():
    path = REPOSITORY_ROOT / "examples"
    for category in path.iterdir():
        if category.is_dir():
            for example in category.iterdir():
                generate(category.name, example.name)


if __name__ == "__main__":
    main()
