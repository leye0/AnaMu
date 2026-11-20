\include "parts-common.ily"

#(set-global-staff-size 16)

\header {
  title = "Giulio Cesare in Egitto"
  composer = "George Frideric Haendel"
  poet = "Nicola Francesco Haym"
  maintainer = "Nicolas Sceaux"

  copyright = \markup { Copyright \maintainer 2005-2006. \hspace #1.0 Licensed 
                        under the Creative Commons Attribution 2.5 License }
  tagline = \markup {
    \override #'(box-padding . 1.0) \override #'(baseline-skip . 2.7)
    \small \box \center-align {
      \line { Copyright \maintainer 2005. \hspace #1.0 Licensed 
              under the Creative Commons Attribution 2.5 License,}
      \line { for details see: 
              \with-url #"http://creativecommons.org/licenses/by/2.5" 
              http://creativecommons.org/licenses/by/2.5
              ~ Typeset using
              \with-url #"http://www.LilyPond.org" \line { \teeny www.LilyPond.org }
              #(ly:export (string-append "version " (lilypond-version))) \hspace #-1 .}
      \line { Sheet music from
              \with-url #"http://www.MutopiaProject.org" \line { \teeny www.MutopiaProject.org} \hspace #-1 ,
              free to download, modify, and perform.
            }
    }
  }
}

%%$\cesareBaryton
%%$\tolomeoBaryton
%%$\nirenoBaryton
%%$\corneliaGClef
#(*mark-top-padding* -4)

\includePartScore "BAAcoro" "reduction"
\includePartScore "BABcesare" "reduction"
\includePartScore "BACrecit" "reduction"
\includePartScore "BBArecit" "reduction"
\includePartScore "BCArecit" "reduction"
\includePartScore "BCBcesare" "reduction"
\includePartScore "BDArecit" "reduction"
\includePartScore "BDBcornelia" "reduction"
\includePartScore "BDCrecit" "reduction"
\includePartScore "BDDsesto" "reduction"
\includePartScore "BEArecit" "reduction"
\includePartScore "BEBcleopatra" "reduction"
\includePartScore "BFArecit" "reduction"
\includePartScore "BFBtolomeo" "reduction"
\includePartScore "BGAcesare" "reduction"
\includePartScore "BGBrecit" "reduction"
\includePartScore "BGCcesare" "reduction"
\includePartScore "BGDrecit" "reduction"
\includePartScore "BGEcleopatra" "reduction"
\includePartScore "BGFrecit" "reduction"
\includePartScore "BHAcornelia" "reduction"
\includePartScore "BHBrecit" "reduction"
\includePartScore "BHCsesto" "reduction"
\includePartScore "BHDrecit" "reduction"
\includePartScore "BHEcleopatra" "reduction"
\includePartScore "BIArecit" "reduction"
\includePartScore "BIBcesare" "reduction"
\includePartScore "BJArecit" "reduction"
\includePartScore "BKArecit" "reduction"
\includePartScore "BKBachilla" "reduction"
\includePartScore "BKCrecit" "reduction"
\includePartScore "BKDcorneliaSesto" "reduction"

\pageBreakNext
\includePartScore "CAArecit" "reduction"
\includePartScore "CBArecit" "reduction"
\includePartScore "CBBsinfonia" "reduction"
\includePartScore "CBCrecit" "reduction"
\markup \opus "[Sinfonia.]"
\includePartScore "CBErecit" "reduction"
\includePartScore "CBFcleopatra" "reduction"
#(*mark-top-padding* 2)
\includePartScore "CBGrecit" "reduction"
#(*mark-top-padding* -4)
\includePartScore "CBHrecit" "reduction"
\includePartScore "CBIcesare" "reduction"
#(*mark-top-padding* 2)
\includePartScore "CCAcornelia" "reduction"
#(*mark-top-padding* -4)
\includePartScore "CCBrecit" "reduction"
\includePartScore "CDArecit" "reduction"
\includePartScore "CDBachilla" "reduction"
\includePartScore "CDCrecit" "reduction"
\includePartScore "CDDtolomeo" "reduction"
\includePartScore "CEArecit" "reduction"
\includePartScore "CFArecit" "reduction"
\includePartScore "CFBcornelia" "reduction"
\includePartScore "CFCrecit" "reduction"
\includePartScore "CFDsesto" "reduction"
\includePartScore "CGArecit" "reduction"
\includePartScore "CGBcleopatra" "reduction"
\includePartScore "CGCrecit" "reduction"
\includePartScore "CHArecit" "reduction"
\includePartScore "CHBcesare" "reduction"
\includePartScore "CHCrecit" "reduction"
\includePartScore "CHDcleopatra" "reduction"
\includePartScore "CIAtolomeo" "reduction"
\includePartScore "CIBrecit" "reduction"
\includePartScore "CJArecit" "reduction"
\includePartScore "CKArecit" "reduction"
\includePartScore "CKBsesto" "reduction"

\pageBreakNext
\includePartScore "DAArecit" "reduction"
\includePartScore "DABachilla" "reduction"
\markup \piece "Scena II."
\markup \opus "[Sinfonia.]"
\includePartScore "DBBrecit" "reduction"
\includePartScore "DBCtolomeo" "reduction"
\includePartScore "DCArecit" "reduction"
\includePartScore "DCBcleopatra" "reduction"
\includePartScore "DDArecit" "reduction"
\includePartScore "DDBcesare" "reduction"
\includePartScore "DDCrecit" "reduction"
\includePartScore "DEArecit" "reduction"
\includePartScore "DEBcesare" "reduction"
\includePartScore "DFArecit" "reduction"
\includePartScore "DFBsesto" "reduction"
\includePartScore "DGAcleopatra" "reduction"
\includePartScore "DGBrecit" "reduction"
\includePartScore "DGCcleopatra" "reduction"
\includePartScore "DHArecit" "reduction"
\includePartScore "DIArecit" "reduction"
\includePartScore "DIBcornelia" "reduction"
\markup \piece "Scena Ultima."
\markup \opus "[Sinfonia.]"
\includePartScore "DJBrecit" "reduction"
\includePartScore "DJCcleopatraCesare" "reduction"
\includePartScore "DJDrecit" "reduction"
\includePartScore "DJEcoro" "reduction"


\markup \fill-line {
  \null
  \override #'(linewidth . 70) \column {
    \fill-line { \huge Contents }
    \fill-line { \vspace #1 }
    \fill-line { \large \italic "Act I." }
    \fill-line { "Coro. Viva il nostre Alcide" 1 }
    \fill-line { "Aria. Cesare: Presti omai l'egizia terra" 6 }
    \fill-line { "Aria. Cesare: Empio, dirò, tu sei" 12 }
    \fill-line { "Aria. Cornelia: Priva son d'ogni conforto" 17 }
    \fill-line { "Aria. Sesto: Svegliatevi nel core" 18 }
    \fill-line { "Aria. Cleopatra: Non disperar, chi sa ?" 23 }
    \fill-line { "Aria. Tolomeo: L'empio, sleale, indegno" 27 }
    \fill-line { "Recit. Cesare: Alma del gran Pompeo" 29 }
    \fill-line { "Aria. Cesare: Non è si vago e bello" 32 }
    \fill-line { "Aria. Cleopatra: Tutto può donna Vezzosa, s'amorosa" 35 }
    \fill-line { "Aria. Cornelia: Nel tuo seno, amico sasso" 39 }
    \fill-line { "Aria. Sesto: Cara speme, questo core tu cominci a lusingar" 43 }
    \fill-line { "Aria. Cleopatra: Tu la mia stella sei, amabile speranza" 46 }
    \fill-line { "Aria. Cesare: Va tacito e nascosto, quand' avido" 50 }
    \fill-line { "Aria. Achilla: Tu sei il cor di questo core" 55 }
    \fill-line { "Aria. Sesto e Cornelia: Son nato a sospirar/Son nata a lagrimar" 60 }
    \fill-line { \vspace #1 }
    \fill-line { \large \italic "Act II." }
    \fill-line { "Aria. Cleopatra: V'adoro, pupile" 65 }
    \fill-line { "Aria. Cesare: Se in fiorito" 68 }
    \fill-line { "Arioso. Cornelia: Deh, piangete, o mesti lumi" 73 }
    \fill-line { "Aria. Achilla: Se a me non sei crudele" 75 }
    \fill-line { "Aria. Tolomeo: Sì, spietata, il tuo rigore" 79 }
    \fill-line { "Aria. Cornelia: Cessa omai di sospirare" 83 }
    \fill-line { "Aria. Sesto: Cara speme, questo core tu cominci a lusingar" 85 }
    \fill-line { "Aria. Cleopatra: Venere bella" 90 }
    \fill-line { "Aria. Cesare: Al lampo dell'armi" 97 }
    \fill-line { "Aria. Cleopatra: Se pietà di me non senti" 102 }
    \fill-line { "Arioso. Tolomeo: Belle dee di questo core" 106 }
    \fill-line { "Aria. Sesto: L'aura che spira" 111 }
    \fill-line { \vspace #1 }
    \fill-line { \large \italic "Act III." }
    \fill-line { "Aria. Achilla: Dal fulgor di questa spada" 117 }
    \fill-line { "Aria. Tolomeo: Domerò la tua fierezza" 121 }
    \fill-line { "Aria. Cleopatra: Piangerò la sorte mia" 125 }
    \fill-line { "Recit. Cesare: Dall' ondoso periglio salvo mi" 127 }
    \fill-line { "Aria. Cesare: Aure, deh, per pietà" 129 }
    \fill-line { "Aria. Cesare: Quel torrente che cade dal monte" 135 }
    \fill-line { "Aria. Sesto: La giustizia ha già sull'arco" 140 }
    \fill-line { "Recit. Cleopatra: Voi, che mie fide ancelle" 143 }
    \fill-line { "Aria. Cleopatra: Da tempeste il legno infranto" 146 }
    \fill-line { "Aria. Cornelia: Non ha più che temere" 153 }
    \fill-line { "Duetto. Cleopatra e Cesare: Caro/Bella, più amabile beltà" 158 }
    \fill-line { "Coro. Ritorni omai nel nostro core" 162 }
  }
  \null
}
