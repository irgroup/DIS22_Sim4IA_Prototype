import os
import sys
import gc
import logging
from utils.progress_indicator import ProgressIndicator
from sims.search_user import SimulatedUser
from sims.conversational_search_user import SimulatedConversationalUser
from utils.config_readers.simulation_config_reader import SimulationConfigReader


def main(config_filename):
    """
    The main simulation!
    For every configuration permutation, create a Simulated user object, and run the simulation (the while loop).
    Then save, report, and repeat ad naseum.
    """
    logging.basicConfig(filename='sim.log',level=logging.DEBUG)
    config_reader = SimulationConfigReader(config_filename)

    for configuration in config_reader:
        if configuration.user.type == 'ConversationalSearchUser':
            user = SimulatedConversationalUser(configuration)
        else:
            user = SimulatedUser(configuration)
        
        progress = ProgressIndicator(configuration)
        configuration.output.display_config()
        
        while not configuration.user.logger.is_finished():
            #progress.update()  # Update the progress indicator in the terminal.
            user.decide_action()
        
        configuration.output.display_report()
        #print "complete."
        configuration.output.save()
        gc.collect()

    completed_file = open(os.path.join(config_reader.get_base_dir(), 'COMPLETED'), 'w')
    completed_file.close()


def usage(script_name):
    """
    Prints the usage message to the output stream.
    """
    print("Usage: {0} [configuration_filename]".format(script_name))


if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 2:
        usage(sys.argv[0])
    else:
        main(sys.argv[1])