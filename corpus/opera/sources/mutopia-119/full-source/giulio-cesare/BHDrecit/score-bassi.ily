\score {
  \new OrchestraStaffGroup <<
    \smallerRecitStaff <<
      \global
      \cleopatra \includeNotes "recit" 
    >> \includeLyrics "lyrics" 
    \instrStaff \markup "" <<
      \scoreInit \global
      \clef bass \includeNotes "bassi"
    >>
  >>
  \header {
    opus = "Recitativo."
    breakbefore = #(break-before?) 
  }
  \layout { indent = \smallindent }
}
