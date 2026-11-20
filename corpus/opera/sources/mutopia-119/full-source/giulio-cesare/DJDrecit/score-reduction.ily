%% Recit.
\score {
  \new OrchestraStaffGroup <<
    \lyricStaff \markup Cesare. <<
      \keepWithTag #'() \global
      \cesare \includeNotes "cesare"
    >> \includeLyrics "cesare-lyrics"

    \instrStaff \markup "" <<
      \keepWithTag #'down \global
      \clef bass
      \includeNotes "bassi"
      \includeFigures "figures"
    >>
  >>
  \header { opus = "Recitativo."
            breakbefore = #(break-before?) }
  \layout {}
}
