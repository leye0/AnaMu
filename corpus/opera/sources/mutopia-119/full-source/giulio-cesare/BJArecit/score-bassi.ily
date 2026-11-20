\score {
  \new OrchestraStaffGroup <<
    \smallerRecitStaff <<
      \keepWithTag #'(recit hack) \global
      \includeNotes "recit"
    >> \includeLyrics "lyrics"
    \instrStaff \markup "" <<
      \scoreInit 
      \keepWithTag #'() \global
      \clef bass \includeNotes "bassi"
      \includeFigures "figures"
    >>
  >>
  \header {
    piece = "Scena X."
    opus = "Recitativo."
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
