"""repositories.sample_interface"""
#########################################################
# Builtin packages
#########################################################
import abc

#########################################################
# 3rd party packages
#########################################################
# (None)

#########################################################
# Own packages
#########################################################
# (None)


class IgRepositoryInterface(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    @abc.abstractmethod
    def get(self):
        raise NotImplementedError()
