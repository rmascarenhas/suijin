"""main: execution entry point.

Most often, this module is not called directly but instead invoked via the
`bin/suijin` shell script available in this project.
"""

import cli

def main():
    arguments = cli.run()
    print('Reading TIF from: {}'.format(arguments.input))
    print('Saving output to: {}'.format(arguments.output))
    print('Applying algorithm: {}'.format(arguments.algorithm))

# entry point of execution: if invoked from `bin/suijin`, run the `main`
# function defined above
if __name__ == '__main__':
    main()
