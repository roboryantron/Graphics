from ...shared.constants import TEST_PROJECTS_DIR, PATH_UNITY_REVISION, PATH_TEST_RESULTS, PATH_PLAYERS, GITHUB_CDS_URL, UNITY_DOWNLOADER_CLI_URL, UTR_INSTALL_URL,get_unity_downloader_cli_cmd
from ...shared.utr_utils import  extract_flags


def _cmd_base(project_folder, platform, utr_flags, editor):
    return [
        f'git clone {GITHUB_CDS_URL}/sophia/URP-Update-testing.git TestProjects/URP-Update-testing',
        f'curl -s {UTR_INSTALL_URL}.bat --output {TEST_PROJECTS_DIR}/URP-Update-testing/{project_folder}/utr.bat',
        f'pip install unity-downloader-cli --index-url {UNITY_DOWNLOADER_CLI_URL} --upgrade',
        f'Xcopy /E /I \"com.unity.render-pipelines.core\" \"{TEST_PROJECTS_DIR}/URP-Update-testing/{project_folder}/Packages/com.unity.render-pipelines.core\" /Y',
        f'Xcopy /E /I \"com.unity.render-pipelines.universal\" \"{TEST_PROJECTS_DIR}/URP-Update-testing/{project_folder}/Packages/com.unity.render-pipelines.universal\" /Y',
        f'Xcopy /E /I \"com.unity.shadergraph\" \"{TEST_PROJECTS_DIR}/URP-Update-testing/{project_folder}/Packages/com.unity.shadergraph\" /Y',
        f'cd {TEST_PROJECTS_DIR}/URP-Update-testing/{project_folder} && unity-downloader-cli { get_unity_downloader_cli_cmd(editor, platform["os"]) } {"".join([f"-c {c} " for c in platform["components"]])} --wait --published-only',
        f'cd {TEST_PROJECTS_DIR}/URP-Update-testing/{project_folder} && utr {" ".join(utr_flags)}'
    ]

def cmd_editmode(project_folder, platform, api, test_platform, editor, build_config, color_space):
    utr_args = extract_flags(test_platform["utr_flags"], platform["name"], api["name"], build_config, color_space, project_folder)
    return  _cmd_base(project_folder, platform, utr_args, editor)


def cmd_playmode(project_folder, platform, api, test_platform, editor, build_config, color_space):
    utr_args = extract_flags(test_platform["utr_flags"], platform["name"], api["name"], build_config, color_space, project_folder)
    return  _cmd_base(project_folder, platform, utr_args, editor)

def cmd_standalone(project_folder, platform, api, test_platform, editor, build_config, color_space):
    utr_args = extract_flags(test_platform["utr_flags"], platform["name"], api["name"], build_config, color_space, project_folder)
    base = [
        f'curl -s {UTR_INSTALL_URL}.bat --output {TEST_PROJECTS_DIR}/{project_folder}/utr.bat',
        f'cd {TEST_PROJECTS_DIR}/{project_folder} && utr {" ".join(utr_args)}'
        ]
    
    return base


def cmd_standalone_build(project_folder, platform, api, test_platform, editor, build_config, color_space):
    utr_args = extract_flags(test_platform["utr_flags_build"], platform["name"], api["name"], build_config, color_space, project_folder)
    return _cmd_base(project_folder, platform, utr_args, editor)
