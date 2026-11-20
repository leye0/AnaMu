%% Recitativo
\score {
  \new OrchestraStaffGroup <<
    \lyricStaff \markup "Sesto." <<
      \keepWithTag #'() \global
      \sesto \includeNotes "sesto" 
    >>
    \includeLyrics "sesto-lyrics" 
    \instrStaff \markup "" <<
      \keepWithTag #'() \global
      \clef bass
      \includeNotes "bassi"
    >>
  >>
  \header { opus = "Recitativo."
            breakbefore = #(break-before?) }
  \layout { }
}
