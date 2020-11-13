- Staff integration tests 2 and 3 for Milestone 6 were failing due to our State wrongly designating the second player in the
player list as the first player to go.

    - The fix was to change `place_avatar` in our State implementation to only look for the first unstuck player once all 
avatars have been placed (as opposed to doing it throughout the placement phase when players may wind up transiently stuck).
Doing pre-emptively resulted in the player list being prematurely shifted and  causing players
to go in the wrong order.

    - unit test: https://github.ccs.neu.edu/CS4500-F20/quintana/blob/8640d11096bace47f44a638e6416aa3ad84ec46f/Fish/Common/tests/state_tests.py#L826-L869
    - fix: https://github.ccs.neu.edu/CS4500-F20/quintana/blob/8640d11096bace47f44a638e6416aa3ad84ec46f/Fish/Common/state.py#L351-L362
    
 
- Staff integration tests 2 and 3 for Milestone 4 were failing because our State implementation did not allow
moves unless all penguins had been placed.
    - The gist of the fix was to remove any checks in `place_avatar` and `move_avatar` about the status of the
    game (which indicated if all avatars had been placed).
    - unit test: https://github.ccs.neu.edu/CS4500-F20/quintana/blob/2ab6084356020116dafca067cde47aca4e4848c4/Fish/Common/tests/state_tests.py#L380-L410
    - fix part 1: https://github.ccs.neu.edu/CS4500-F20/wellman/commit/06b285e749135677b54370a7ece5d2c80cb4704a#diff-3c0c742881289081d1c3cfb361c6da0eL371-L374
        - you might have to scroll down to 'state.py' and expand as git won't unravel / pan automatically
    - fix part 2: https://github.ccs.neu.edu/CS4500-F20/wellman/commit/06b285e749135677b54370a7ece5d2c80cb4704a#diff-3c0c742881289081d1c3cfb361c6da0eL315-L320
        - you might have to scroll down to 'state.py' and expand as git won't unravel / pan automatically
