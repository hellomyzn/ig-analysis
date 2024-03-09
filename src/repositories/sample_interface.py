"""repositories.sample_interface"""
#########################################################
# Builtin packages
#########################################################
import abc

#########################################################
# 3rd party packages
#########################################################

#########################################################
# Own packages
#########################################################


class SampleRepoInterface(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    @abc.abstractmethod
    def all(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def find_by_id(self, id: int):
        raise NotImplementedError()

    @abc.abstractmethod
    def add(self, data: dict):
        raise NotImplementedError()

    @abc.abstractmethod
    def delete_by_id(self, id: int):
        raise NotImplementedError()
