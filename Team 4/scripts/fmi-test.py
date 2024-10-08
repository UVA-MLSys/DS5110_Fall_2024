import fmi
import sys
import numpy as np
import os
import argparse


def environ_or_required(key):
    return (
        {'default': os.environ.get(key)} if os.environ.get(key)
        else {'required': True}
    )


def fmi_test(data=None):
    world_size = int(data["world_size"])
    rank = int(data["rank"])
    comm = fmi.Communicator(rank, world_size, "fmi.json", "fmi_pair", 512)

    comm.hint(fmi.hints.fast)

    comm.barrier()

    if rank == 0:
        # send / recv
        comm.send(42, 1, fmi.types(fmi.datatypes.int))
        comm.send(14.2, 1, fmi.types(fmi.datatypes.double))
        comm.send([1, 2], 1, fmi.types(fmi.datatypes.int_list, 2))
        comm.send([1.32, 2.34], 1, fmi.types(fmi.datatypes.double_list, 2))
        # bcast
        comm.bcast(42, 0, fmi.types(fmi.datatypes.int))
        comm.bcast(14.2, 0, fmi.types(fmi.datatypes.double))
        comm.bcast([1, 2], 0, fmi.types(fmi.datatypes.int_list, 2))
        comm.bcast([1.32, 2.34], 0, fmi.types(fmi.datatypes.double_list, 2))
        # gather
        print(comm.gather(1, 0, fmi.types(fmi.datatypes.int)))
        print(comm.gather(14.5, 0, fmi.types(fmi.datatypes.double)))
        print(comm.gather([1, 2], 0, fmi.types(fmi.datatypes.int_list, 2)))
        print(comm.gather([1.32, 2.34], 0, fmi.types(fmi.datatypes.double_list, 2)))
        # scatter
        print(comm.scatter([14, 42], 0, fmi.types(fmi.datatypes.int_list, 2)))
        print(comm.scatter([1.3, 2.3, 3.3, 4.3], 0, fmi.types(fmi.datatypes.double_list, 4)))
        # reduce
        print(comm.reduce(42, 0, fmi.func(fmi.op.sum), fmi.types(fmi.datatypes.int)))
        print(comm.reduce(14.0, 0, fmi.func(fmi.op.prod), fmi.types(fmi.datatypes.double)))
        print(comm.reduce(42, 0, fmi.func(fmi.op.max), fmi.types(fmi.datatypes.int)))
        print(comm.reduce(41.0, 0, fmi.func(fmi.op.min), fmi.types(fmi.datatypes.double)))
        print(comm.reduce(42, 0, fmi.func(fmi.op.custom, lambda a, b: 2 * a + 2 * b, True, True),
                          fmi.types(fmi.datatypes.int)))
        print(comm.reduce(0.1, 0, fmi.func(fmi.op.custom, lambda a, b: 2 * a + 2 * b, True, True),
                          fmi.types(fmi.datatypes.double)))
        print(comm.reduce([42, 14], 0, fmi.func(fmi.op.sum), fmi.types(fmi.datatypes.int_list, 2)))
        print(comm.reduce([42, 14], 0, fmi.func(fmi.op.prod), fmi.types(fmi.datatypes.int_list, 2)))
        print(comm.reduce([43.5, 13.5], 0, fmi.func(fmi.op.max), fmi.types(fmi.datatypes.double_list, 2)))
        print(comm.reduce([41.5, 15.5], 0, fmi.func(fmi.op.min), fmi.types(fmi.datatypes.double_list, 2)))
        print(comm.reduce([42, 14], 0, fmi.func(fmi.op.custom, lambda a, b: 2 * a + 2 * b, True, True),
                          fmi.types(fmi.datatypes.int_list, 2)))
        # allreduce
        print(comm.allreduce(42, fmi.func(fmi.op.sum), fmi.types(fmi.datatypes.int)))
        print(comm.allreduce(14.0, fmi.func(fmi.op.prod), fmi.types(fmi.datatypes.double)))
        print(comm.allreduce(42, fmi.func(fmi.op.max), fmi.types(fmi.datatypes.int)))
        print(comm.allreduce(41.0, fmi.func(fmi.op.min), fmi.types(fmi.datatypes.double)))
        print(comm.allreduce(42, fmi.func(fmi.op.custom, lambda a, b: 2 * a + 2 * b, True, True),
                             fmi.types(fmi.datatypes.int)))
        print(comm.allreduce(0.1, fmi.func(fmi.op.custom, lambda a, b: 2 * a + 2 * b, True, True),
                             fmi.types(fmi.datatypes.double)))
        print(comm.allreduce([42, 14], fmi.func(fmi.op.sum), fmi.types(fmi.datatypes.int_list, 2)))
        # scan
        print(comm.scan(42, fmi.func(fmi.op.sum), fmi.types(fmi.datatypes.int)))
        print(comm.scan(14.0, fmi.func(fmi.op.prod), fmi.types(fmi.datatypes.double)))
        print(comm.scan(42, fmi.func(fmi.op.max), fmi.types(fmi.datatypes.int)))
        print(comm.scan(41.0, fmi.func(fmi.op.min), fmi.types(fmi.datatypes.double)))
        print(comm.scan(42, fmi.func(fmi.op.custom, lambda a, b: 2 * a + 2 * b, True, True),
                        fmi.types(fmi.datatypes.int)))
        print(comm.scan(0.1, fmi.func(fmi.op.custom, lambda a, b: 2 * a + 2 * b, True, True),
                        fmi.types(fmi.datatypes.double)))
        print(comm.scan([42, 14], fmi.func(fmi.op.sum), fmi.types(fmi.datatypes.int_list, 2)))

    elif rank == 1:
        # send / recv
        print(comm.recv(0, fmi.types(fmi.datatypes.int)))
        print(comm.recv(0, fmi.types(fmi.datatypes.double)))
        print(comm.recv(0, fmi.types(fmi.datatypes.int_list, 2)))
        print(comm.recv(0, fmi.types(fmi.datatypes.double_list, 2)))
        # bcast
        print(comm.bcast(None, 0, fmi.types(fmi.datatypes.int)))
        print(comm.bcast(None, 0, fmi.types(fmi.datatypes.double)))
        print(comm.bcast(None, 0, fmi.types(fmi.datatypes.int_list, 2)))
        print(comm.bcast(None, 0, fmi.types(fmi.datatypes.double_list, 2)))
        # gather
        comm.gather(2, 0, fmi.types(fmi.datatypes.int))
        comm.gather(42.5, 0, fmi.types(fmi.datatypes.double))
        comm.gather([3, 4], 0, fmi.types(fmi.datatypes.int_list, 2))
        comm.gather([3.32, 4.34], 0, fmi.types(fmi.datatypes.double_list, 2))
        # scatter
        print(comm.scatter(None, 0, fmi.types(fmi.datatypes.int_list, 2)))
        print(comm.scatter(None, 0, fmi.types(fmi.datatypes.double_list, 4)))
        # reduce
        comm.reduce(42, 0, fmi.func(fmi.op.sum), fmi.types(fmi.datatypes.int))
        comm.reduce(14.0, 0, fmi.func(fmi.op.prod), fmi.types(fmi.datatypes.double))
        comm.reduce(43, 0, fmi.func(fmi.op.max), fmi.types(fmi.datatypes.int))
        comm.reduce(41.0, 0, fmi.func(fmi.op.min), fmi.types(fmi.datatypes.double))
        comm.reduce(42, 0, fmi.func(fmi.op.custom, lambda a, b: 2 * a + 2 * b, True, True),
                    fmi.types(fmi.datatypes.int))
        comm.reduce(0.2, 0, fmi.func(fmi.op.custom, lambda a, b: 2 * a + 2 * b, True, True),
                    fmi.types(fmi.datatypes.double))
        comm.reduce([42, 14], 0, fmi.func(fmi.op.sum), fmi.types(fmi.datatypes.int_list, 2))
        comm.reduce([42, 14], 0, fmi.func(fmi.op.prod), fmi.types(fmi.datatypes.int_list, 2))
        comm.reduce([43.5, 13.5], 0, fmi.func(fmi.op.max), fmi.types(fmi.datatypes.double_list, 2))
        comm.reduce([41.5, 15.5], 0, fmi.func(fmi.op.min), fmi.types(fmi.datatypes.double_list, 2))
        comm.reduce([42, 14], 0, fmi.func(fmi.op.custom, lambda a, b: 2 * a + 2 * b, True, True),
                    fmi.types(fmi.datatypes.int_list, 2))
        # allreduce
        print(comm.allreduce(42, fmi.func(fmi.op.sum), fmi.types(fmi.datatypes.int)))
        print(comm.allreduce(14.0, fmi.func(fmi.op.prod), fmi.types(fmi.datatypes.double)))
        print(comm.allreduce(42, fmi.func(fmi.op.max), fmi.types(fmi.datatypes.int)))
        print(comm.allreduce(41.0, fmi.func(fmi.op.min), fmi.types(fmi.datatypes.double)))
        print(comm.allreduce(42, fmi.func(fmi.op.custom, lambda a, b: 2 * a + 2 * b, True, True),
                             fmi.types(fmi.datatypes.int)))
        print(comm.allreduce(0.1, fmi.func(fmi.op.custom, lambda a, b: 2 * a + 2 * b, True, True),
                             fmi.types(fmi.datatypes.double)))
        print(comm.allreduce([42, 14], fmi.func(fmi.op.sum), fmi.types(fmi.datatypes.int_list, 2)))
        # scan
        print(comm.scan(42, fmi.func(fmi.op.sum), fmi.types(fmi.datatypes.int)))
        print(comm.scan(14.0, fmi.func(fmi.op.prod), fmi.types(fmi.datatypes.double)))
        print(comm.scan(42, fmi.func(fmi.op.max), fmi.types(fmi.datatypes.int)))
        print(comm.scan(41.0, fmi.func(fmi.op.min), fmi.types(fmi.datatypes.double)))
        print(comm.scan(42, fmi.func(fmi.op.custom, lambda a, b: 2 * a + 2 * b, True, True),
                        fmi.types(fmi.datatypes.int)))
        print(comm.scan(0.1, fmi.func(fmi.op.custom, lambda a, b: 2 * a + 2 * b, True, True),
                        fmi.types(fmi.datatypes.double)))
        print(comm.scan([42, 14], fmi.func(fmi.op.sum), fmi.types(fmi.datatypes.int_list, 2)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="fmi scaling")

    parser.add_argument('-r', dest='rank', type=int, **environ_or_required('RANK'))

    parser.add_argument('-w', dest='world_size', type=int, help="world size", **environ_or_required('WORLD_SIZE'))

    args = vars(parser.parse_args())

    print("executing fmi_test operation")
    fmi_test(args)