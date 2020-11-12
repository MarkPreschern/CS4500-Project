- Staff integration tests 2 and 3 for Milestone 6 were failing due to our State wrongly designating the second player in the
player list as the first player to go.

    - The fix was to change `place_avatar` in our State implementation to only look for the first unstuck player once all 
avatars have been placed (as opposed to doing it throughout the placement phase when players may wind up transiently stuck).
Doing pre-emptively resulted in the player list being prematurely shifted and  causing players
to go in the wrong order.

    - unit test: https://github.ccs.neu.edu/CS4500-F20/quintana/blob/8640d11096bace47f44a638e6416aa3ad84ec46f/Fish/Common/tests/state_tests.py#L826-L869
    - fix: https://github.ccs.neu.edu/CS4500-F20/quintana/blob/8640d11096bace47f44a638e6416aa3ad84ec46f/Fish/Common/state.py#L351-L362