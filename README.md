rapidpatch: Tool to create RPM patch effectively
================================================

    Usage: rapidpatch action [ params ]

Helper tool for creating patch for a package and check whether it compiles, that all with strong focus on effectivity. The tool generates a mock config, prepares directory for dependencies available only locally, allows to create patch from unpacked source easily. The tool also allows to run only specific section (or part of it) of the RPM Spec file, which makes the whole testing faster, especially in case of large projects, that compile long time. The tool also supports test-driven development, so ideally packager writes a simple test before writing the patch.

    Actions:
        mock_init        Initializes mock chroot from current branch name.
        mock_pass        Run arbitrary mock command, options will be passed to the mock itself, so
                         for example --shell gives an interactive console.
        mock_shell       Run an interactive console in the mock.
        mock_run         Run any command in the mock buildroot.
        section_build [ --show [ <num> ] | --from <num> | complete ]
                         Without arguments it runs the %build section only. With --show option,
                         user can see line numbers in %build section. With --from option, only
                         part of the %build section can be run
        section_install [ --show [ <num> ] | --from <num> | complete ]
                         Similar semantics as section_build, just for %install section.
        section_files    Run the %files section only.
        run_check <test_script>
                         Runs after-compile-check test, where user can check whatever is needed
                         after compiling (%build section).
        run_check_output <test_script>
                         Runs after-build-check test, where user can check whatever is needed after
                         complete build. Script can expect RPM files and also unpacked RPM files
                         in the current directory.
        update_spec      Copy locally changed SPEC to the mock buildroot.
        generate_patch   Get the changes in the source and store them into the <branch_name>.patch file.

## Example:

This following example shows how to use this tool for package mariadb, which takes long to compile:


### Initializing the mock environment and writing the reproducer

Start with cloning the package as usually, using fedpkg. Create a private branch for this issue.
    
    fedpkg clone mariadb
    cd mariadb
    git checkout -b private-patching-bz1234

For saving time, take a look at whether there are no long running tests during build, and consider temporarily turn them off.

Create a simple test for the issue and store it either as executable script (e.g. reproducer). If written well, it should fail before the issue is fixed.

    cat >reproducer <<EOF
    #!/bin/bash
    set -xe
    client/mysql --help | grep max-allowed-packet
    EOF

After a test is written, we can initialize the mock and try build the package:

    rapidpatch mock_init
    rapidpatch run_check reproducer

We should see test failure, if not, write the test, so it fails when the issue is not fixed.


### Fixing the code of the component

Now, we can change either RPM spec or code in local directory (it is a symlink to the mock directory), both in local directory:

    vim *spec
    vim mariadb-10.1.21/sql/sql_parse.cc
    ...

After fixing the code, we want to run only make command and further commands from the %build section, so let's see how the %build section looks:

    rapidpatch section_build --show

We see that make is run on line #4, so let's continue from here

    rapidpatch section_build --from 4

Now we need to work with the code until the %build section passes and then run the compile check again:

    rapidpatch section_build --from 4
    rapidpatch run_check after-compile-check

After %build section passes, we can continue with %install section

    rapidpatch section_install


### Fixing the %install and %files sections in the RPM spec

In case the the %install section fails, fix the problem in the the RPM spec or code, still in local directory; then run the %install again (we can continue from some line as well):

    rapidpatch section_install 20

We can also re-run the whole install section:

    rapidpatch section_install complete

In case there are some issues in the %files sections, fix them in the RPM spec and re-run the same command:

    rapidpatch section_files

After %install and %files sections finish, run the final check if required (for example when there was problem with RPM metadata):

    rapidpatch run_check_output output-check

Now we can generate the patch and continue as usually

    rapidpatch generate_patch
    git add *.patch
    git commit -a -m 'Some message'
