%% Recitativo
\score {
  \new OrchestraStaffGroup <<
    \lyricStaff \markup Cleopatra. <<
      \keepWithTag #'recit \global
      \cleopatra \includeNotes "cleopatra"
    >> \includeLyrics "cleopatra-lyrics"
    \instrStaff \markup "" <<
      \keepWithTag #'down \global
      \clef bass
      \includeNotes "bassi"
    >>
  >>
  \header {
    piece = "Scena III."
    opus = "Recitativo."
    breakbefore = #(break-before?)
  }
  \layout { }
}
