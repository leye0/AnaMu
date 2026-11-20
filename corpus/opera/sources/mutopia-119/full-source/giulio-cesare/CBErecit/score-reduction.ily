%% Recitativo
\score {
  \new OrchestraStaffGroup <<
    \lyricStaff \markup Cesare. <<
      \keepWithTag #'recit \global
      \includeNotes "recit"
    >> \includeLyrics "lyrics"
    \instrStaff \markup "" <<
      \keepWithTag #'down \global
      \clef bass
      \includeNotes "bassi"
    >>
  >>
  \header { opus = "Recitativo."
            breakbefore = #(break-before?) }
  \layout { }
}
