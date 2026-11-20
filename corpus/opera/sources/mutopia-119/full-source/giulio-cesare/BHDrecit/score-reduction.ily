%% Recitativo.
\score {
  \new OrchestraStaffGroup <<
    \lyricStaff \markup "Cleopatra." <<
      \global
      \cleopatra \includeNotes "recit" 
    >> \includeLyrics "lyrics" 
    \instrStaff \markup "" <<
      \global
      \clef bass
      \includeNotes "bassi"
    >>
  >>
  \header { opus = "Recitativo."
            breakbefore = #(break-before?) }
  \layout { }
}
