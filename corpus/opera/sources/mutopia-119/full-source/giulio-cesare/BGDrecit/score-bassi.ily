\score {
  \new OrchestraStaffGroup <<
    \smallerRecitStaff <<
      \global \includeNotes "recit"
    >> \includeLyrics "lyrics"
    \instrStaff \markup "" <<
      \scoreInit \global
      \clef bass \includeNotes "bassi"
      \includeFigures "figures"
    >>
  >>
  \header {
    opus = "Recitativo."
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
