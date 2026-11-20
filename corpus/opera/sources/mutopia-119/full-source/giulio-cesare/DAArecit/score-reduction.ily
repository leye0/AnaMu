%% Recitativo
\score {
  \new OrchestraStaffGroup <<
    \lyricStaff \markup Achilla. <<
      \keepWithTag #'recit  \global
      \achilla \includeNotes "achilla"
    >> \includeLyrics "achilla-lyrics"
    \instrStaff \markup "" <<
      \keepWithTag #'down \global
      \clef bass
      \includeNotes "bassi"
    >>
  >>
  \header {
    piece = "Atto Terzo, Scena I."
    opus = "Recitativo."
    breakbefore = #(break-before?)
  }
  \layout { }
}
