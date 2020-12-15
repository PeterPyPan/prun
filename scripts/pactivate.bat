@ECHO off
FOR /F "tokens=* USEBACKQ" %%F IN (`prun activate`) DO (
%%F
)