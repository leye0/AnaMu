%% Recitativo
\score {
  \new OrchestraStaffGroup <<
    \lyricStaff \markup Sesto. <<
      \keepWithTag #'up  \global
      \sesto \includeNotes "sesto"
    >> \includeLyrics "sesto-lyrics"
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
