"""main: execution entry point.

Most often, this module is not called directly but instead invoked via the
`bin/suijin` shell script available in this project.
"""

import cli
import hydro

def main():
    arguments = cli.run()

    if arguments.algorithm == 'direction':
        algo = hydro.Direction(arguments.input)

    algo.run(arguments.output)

# entry point of execution: if invoked from `bin/suijin`, run the `main`
# function defined above
if __name__ == '__main__':
    main()
