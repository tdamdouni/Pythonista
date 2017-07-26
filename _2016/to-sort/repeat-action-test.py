# https://forum.omz-software.com/topic/3170/action-repeat-won-t-repeat/2

up = A.move_to(self.size.w/2, 350, 9, TIMING_EASE_BACK_OUT)
d = 2.0 # duration
# Inline function for the call action:
def move_random():
  x, y = random.randrange(100,924), random.randrange(300,700)
  self.boss.run_action(A.move_to(x, y, d))
# The call action doesn't wait until the move action finishes, so add a wait action for that:
repmo = A.repeat(A.sequence(A.call(move_random), A.wait(d)), -1))
phase_1 = A.sequence(stationary, up)
mo = A.move_to(, 2, TIMING_EASE_BACK_IN_OUT)
self.boss.run_action(A.sequence(phase_1, repmo))
