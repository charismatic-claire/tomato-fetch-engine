#!/bin/sh

# Run Python script
run_python_script() {
	echo "Running Python script"
	PYTHONPATH=$(pwd) python3 src/org/cumcubble/tomatos/MainProgram.py
}

# Create archive to export
create_archive() {
	echo "Creating archive to export"
	rm -fv res/tomatos01.json res/tomatos02.json res/tomatos03.json res/tomatos04.json
	mv -v res/tomatos05.json res/tomatos.json
	tar czf res.tar.gz res
}

# Main program
run_python_script
create_archive
echo; echo "Done."
