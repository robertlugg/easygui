import easygui
import easygui.global_state
from easygui import multenterbox
from tests import WAIT_0_MILLISECONDS


def test__multenterbox__cancel_results_in_run_returning_none():
    meb = multenterbox(msg="test msg", title="test title",
                                fields=['f1', 'f2'], values=['v1', 'v2'],
                                callback=None, run=False)

    def simulate_user_cancel_press(meb_instance):
        meb_instance._cancel_pressed('ignored button handler arg')

    meb.boxRoot.after(WAIT_0_MILLISECONDS, simulate_user_cancel_press, meb)
    actual = meb.run()
    assert actual is None
