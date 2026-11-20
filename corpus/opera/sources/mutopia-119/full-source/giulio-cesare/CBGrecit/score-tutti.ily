%% Recitativo
\score {
  \new Staff <<
    \set Score.skipBars = ##t
    \keepWithTag #'partBoth \global
    { \clef treble \noPageBreak R1*3 R1*5/4 }
  >>
  \header { breakbefore = #(break-before?) }
  \layout { indent = \noindent }
}
