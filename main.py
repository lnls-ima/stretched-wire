"""Run the stretched wire main application."""

from stretchedwire.gui import stretchedwireapp

_run_in_thread = True

if _run_in_thread:
    thread = stretchedwireapp.run_in_thread()
else:
    stretchedwireapp.run()
