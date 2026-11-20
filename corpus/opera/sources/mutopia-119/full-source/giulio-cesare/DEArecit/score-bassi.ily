\score {
  \new OrchestraStaffGroup <<
    \smallerRecitStaff <<
      \keepWithTag #'recit  \global
      \includeNotes "recit"
    >> \includeLyrics "lyrics"
    \instrStaff \markup "" <<
      \scoreInit
      \keepWithTag #'partDown \global
      { s2 s1*3 \break }
      \clef bass
      \includeNotes "bassi"
      \includeFigures "figures"
    >>
  >>
  \header {
    piece = "Scena V."
    opus = "Recitativo."
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
