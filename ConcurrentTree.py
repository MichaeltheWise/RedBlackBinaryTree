# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 2021

@author: Michael Lin
"""
import asyncio
import multiprocessing
import random
import time
from threading import current_thread

import rx
from rx.scheduler import ThreadPoolScheduler
from rx import operators as ops

from RedBlackBinaryTree.RedBlackBinaryTree import RedBlackBinaryTree


def pause_thread(value):
    time.sleep(random.randint(5, 20) * 0.1)
    return value


# Using asyncio to implement
async def request_asyncio(tree, number):
    await asyncio.sleep(1.0)
    return number in tree


async def check_tree_asyncio(tree, number):
    response = await request_asyncio(tree, number)
    print("Result is: {}".format(response))

# Calculate the number of CPUs, then create a ThreadPoolScheduler with that number of threads
optimal_thread_count = multiprocessing.cpu_count()
# print(optimal_thread_count)
pool_scheduler = ThreadPoolScheduler(optimal_thread_count)


def main():
    # Trying out multiprocessing in python using reactive programming
    rb_test_tree = RedBlackBinaryTree()
    rb_test_tree.insert(55)
    rb_test_tree.insert(40)
    rb_test_tree.insert(30)
    rb_test_tree.insert(35)

    # Process 1: Inorder Traversal
    rx.from_list(rb_test_tree.inorder_print_tree()).pipe(
        ops.map(lambda s: pause_thread(s)), ops.subscribe_on(pool_scheduler)
    ).subscribe(
        on_next=lambda s: print("PROCESS 1: {0} {1}".format(current_thread().name, s)),
        on_error=lambda e: print(e),
        on_completed=lambda: print("PROCESS 1 done!"),
    )

    # Process 2: Preorder Traversal
    rx.from_list(rb_test_tree.preorder_print_tree()).pipe(
        ops.map(lambda s: pause_thread(s)), ops.subscribe_on(pool_scheduler)
    ).subscribe(
        on_next=lambda s: print("PROCESS 2: {0} {1}".format(current_thread().name, s)),
        on_error=lambda e: print(e),
        on_completed=lambda: print("PROCESS 2 done!"),
    )

    # Process 3: Postorder Traversal
    rx.from_list(rb_test_tree.postorder_print_tree()).pipe(
        ops.map(lambda s: pause_thread(s)), ops.subscribe_on(pool_scheduler)
    ).subscribe(
        on_next=lambda s: print("PROCESS 3: {0} {1}".format(current_thread().name, s)),
        on_error=lambda e: print(e),
        on_completed=lambda: print("PROCESS 3 done!"),
    )

    # Process 4: Graphical printing
    rx.of(rb_test_tree.graphicalPrintTree()).pipe(
        ops.map(lambda s: pause_thread(s)), ops.subscribe_on(pool_scheduler)
    ).subscribe(
        on_next=lambda s: print("PROCESS 4: {0} {1}".format(current_thread().name, s)),
        on_error=lambda e: print(e),
        on_completed=lambda: print("PROCESS 4 done!"),
    )

    # Process 5: Check using coroutines
    loop = asyncio.get_event_loop()
    loop.run_until_complete(check_tree_asyncio(rb_test_tree, 30))
    loop.run_until_complete(check_tree_asyncio(rb_test_tree, 65))
    # Can also schedule this by doing it this way
    # asyncio.gather(*[check_tree_asyncio(rb_test_tree, 30), check_tree_asyncio(rb_test_tree, 65)])
    # This collects the calls simultaneously
    # or
    # asyncio.ensure_future(check_tree_asyncio(rb_test_tree, 30))
    # asyncio.ensure_future(check_tree_asyncio(rb_test_tree, 65))
    # This schedules the calls
    # loop.run_forever()
    # Run forever needs manually break

    # Output looks like this as expected:
    # All the processes are concurrently running

    # PROCESS 1: ThreadPoolExecutor-0_0 30
    # Result is: True
    # PROCESS 4: ThreadPoolExecutor-0_3
    # defaultdict(<class 'list'>, {40: [(30, 'Black'), (55, 'Black')], 30: [(35, 'Red')]})
    # PROCESS 4 done!
    # PROCESS 3: ThreadPoolExecutor-0_2 35
    # PROCESS 2: ThreadPoolExecutor-0_1 40
    # PROCESS 3: ThreadPoolExecutor-0_2 30
    # Result is: False
    # PROCESS 1: ThreadPoolExecutor-0_0 35
    # PROCESS 3: ThreadPoolExecutor-0_2 55
    # PROCESS 2: ThreadPoolExecutor-0_1 30
    # PROCESS 1: ThreadPoolExecutor-0_0 40
    # PROCESS 2: ThreadPoolExecutor-0_1 35
    # PROCESS 3: ThreadPoolExecutor-0_2 40
    # PROCESS 3 done!
    # PROCESS 1: ThreadPoolExecutor-0_0 55
    # PROCESS 1 done!
    # PROCESS 2: ThreadPoolExecutor-0_1 55
    # PROCESS 2 done!


if __name__ == '__main__':
    main()
