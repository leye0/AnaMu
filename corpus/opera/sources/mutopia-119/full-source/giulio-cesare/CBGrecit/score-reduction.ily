%% Recitativo
\score {
  \new OrchestraStaffGroup <<
    \lyricStaff \markup Cesare. <<
      \keepWithTag #'up \global
      \cesare \includeNotes "recit"
    >> \includeLyrics "lyrics"
    \instrStaff \markup "" <<
      \keepWithTag #'down \global
      \clef bass
      \includeNotes "bassi"
      \includeFigures "figures"
    >>
  >>
  \header { opus = "Recitativo."
            breakbefore = #(break-before?) }
  \layout { }
}
