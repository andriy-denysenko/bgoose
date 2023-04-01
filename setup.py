import cx_Freeze

executables = [cx_Freeze.Executable("asteroeat.pyw")]

cx_Freeze.setup(
    name="АстероЇд",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["player.png", "meanie.png", "bonus.png", "bg.png"]}},
    executables = executables

    )