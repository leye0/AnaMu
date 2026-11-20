%% Aria. Cleopatra: Piangerò la sorte mia
\score {
  <<
    \lyricStaff \markup Cleopatra. <<
      \keepWithTag #'partUp \global
      {
        \cleopatra \includeNotes "cleopatra-1" 
        \cleopatra \includeNotes "cleopatra-2" 
      }
    >> { 
      \includeLyrics "cleopatra-lyrics-1"
      \includeLyrics "cleopatra-lyrics-2" 
    }
    
    \new PianoStaff <<
      \new Staff <<
        \keepWithTag #'() \global
        \clef treble
        {
          \set Staff.printPartCombineTexts = ##f
          \partcombine \includeNotes "violino1-1" \includeNotes "violino2-1"
          \includeNotes "violini-2"
        }
      >>
      \new Staff <<
        \keepWithTag #'partDown \global
        \clef bass
        {
          \includeNotes "bassi-1"
          << \includeNotes "cello-2" \includeFigures "figures-2" >>
        }
      >>
    >>
  >>
  \header { opus = "Aria. Cleopatra: Piangerò la sorte mia"
            breakbefore = #(break-before?) }
  \layout { }
}
