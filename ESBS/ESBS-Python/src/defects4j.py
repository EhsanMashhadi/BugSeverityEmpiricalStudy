import os
import subprocess


def get_project_urls(project_name):
    result = subprocess.run(['defects4j', 'query', '-p', project_name, "-q", "report.url"],
                            stdout=subprocess.PIPE)
    return result.stdout.decode("utf-8").strip().split("\n")


def get_project_ids(project_name):
    result = subprocess.run(['defects4j', 'query', '-p', project_name],
                            stdout=subprocess.PIPE)
    return result.stdout.decode("utf-8").strip().split("\n")


def checkout_project(project_name, version, output):
    result = subprocess.run(['defects4j', 'checkout', "-p", project_name, "-v", version, "-w", output],
                            stdout=subprocess.PIPE)
    return result.returncode


def get_buggy_files(directory):
    result = subprocess.run(['defects4j', 'export', '-p', 'classes.modified'], cwd=directory,
                            stdout=subprocess.PIPE)
    return result.stdout.decode("utf-8").strip().split("\n")


def compile_project(directory):
    os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"
    result = subprocess.run(['defects4j', 'compile'], cwd=directory,
                            stdout=subprocess.PIPE)
    return result.returncode


def get_project_target(directory):
    result = subprocess.run(['defects4j', 'export', '-p', 'dir.bin.classes'], cwd=directory,
                            stdout=subprocess.PIPE)
    return result.stdout.decode("utf-8").strip().split("\n")[0]


def get_project_classpath(directory):
    result = subprocess.run(['defects4j', 'export', '-p', 'cp.compile'], cwd=directory,
                            stdout=subprocess.PIPE)
    return result.stdout.decode("utf-8").strip()


def get_src_classes(base_directory):
    result = subprocess.run(['defects4j', 'export', "-p", "dir.src.classes"], cwd=base_directory,
                            stdout=subprocess.PIPE)
    return result.stdout.decode("utf-8").strip().split("\n")


def get_buggy_commit(project_name, project_version):
    result = subprocess.run(['defects4j', 'query', '-p', project_name, "-q", "revision.id.buggy"],
                            stdout=subprocess.PIPE)
    row = result.stdout.decode("utf-8").strip().split("\n")
    for id_commit in row:
        version = id_commit.split(",")[0]
        buggy_commit = id_commit.split(",")[1]

        if int(version) == project_version:
            return buggy_commit