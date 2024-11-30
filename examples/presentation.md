---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: "1.3"
      jupytext_version: 1.16.4
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

## <!-- #region editable=true slideshow={"slide_type": "skip"} -->

math: '\CARA': '\alpha' '\CRRA': '\rho' '\PtyLab': '\mathrm{Z}' '\ptyLab': "z"
'\TaxComb': '\mathcal{T}' '\Prob': '\mathbb{P}' '\DiePrb': '\mathsf{D}'
'\diePrb': '\mathsf{d}' '\LivPrb': '\cancel{\DiePrb}' '\livPrb':
'\cancel{\diePrb}' '\DiscFac': '\beta' '\DieFac': '\pDead' '\GroFac': '\Omega'
'\BalGroFac': '\check' '\permGroFac': '\Gamma' '\PermGroFac': '\pmb{\Phi}'
'\PopnGroFac': '\Xi' '\APFac': '\text{\pmb{\Thorn}}' '\PopFac': '\PopGro'
'\RPFac': '\APFac*{\Rfree}' '\DeprFac': '\daleth' '\LivFac': '\Alive' '\aVec':
'\vec{\mathrm{a}}' '\bVec': '\vec{\mathrm{\bNrm}}' '\cVec':
'\vec{\mathrm{\cNrm}}' '\mVec': '\vec{\mathrm{m}}' '\yVec':
'\vec{\mathrm{\yNrm}}' '\Inc': "Y" '\inc': "y" '\PInc': "P" '\AFunc':
'\mathrm{A}' '\aFunc': '\mathrm{a}' '\BFunc': '\mathrm{B}' '\bFunc':
'\mathrm{b}' '\CFunc': '\mathrm{C}' '\cFunc': '\mathrm{c}' '\MPCFunc':
'\pmb{\kappa}' '\DFunc': '\mathrm{D}' '\dFunc': '\mathrm{d}' '\bEndFunc':
'\mathfrak{b}' '\CEndFunc': '\mathfrak{C}' '\cEndFunc': '\mathfrak{c}'
'\dEndFunc': '\mathfrak{d}' '\lEndFunc': '\mathfrak{l}' '\mEndFunc':
'\mathfrak{m}' '\nEndFunc': '\mathfrak{n}' '\VEndFunc': '\mathfrak{V}'
'\vEndFunc': '\mathfrak{v}' '\zEndFunc': '\mathfrak{z}' '\ProdFunc':
'\mathrm{F}' '\prodFunc': '\mathrm{f}' '\EFunc': '\mathrm{E}' '\eFunc':
'\mathrm{e}' '\FFunc': '\mathrm{F}' '\fFunc': '\mathrm{f}' '\GFunc':
'\mathrm{G}' '\gFunc': '\mathrm{g}' '\vBegFunc': '\pmb{\upsilon}' '\HFunc':
'\mathrm{H}' '\hFunc': '\mathrm{h}' '\IFunc': '\mathrm{I}' '\iFunc':
'\mathrm{i}' '\chiFunc': '\pmb{\chi}' '\phiFunc': '\digamma' '\JFunc':
'\mathrm{J}' '\jFunc': '\mathrm{j}' '\KFunc': '\mathrm{K}' '\kFunc':
'\mathrm{k}' '\LFunc': '\mathrm{L}' '\utilFunc': '\mathrm{u}' '\MFunc':
'\mathrm{M}' '\mFunc': '\mathrm{m}' '\NFunc': '\mathrm{N}' '\nFunc':
'\mathrm{n}' '\OFunc': '\mathrm{O}' '\PFunc': '\mathrm{P}' '\pFunc':
'\mathrm{p}' '\QFunc': '\mathrm{Q}' '\RFunc': '\mathrm{R}' '\rFunc':
'\mathrm{r}' '\SFunc': '\mathrm{S}' '\sFunc': '\mathrm{s}' '\MPSFunc':
'\pmb{lambda}' '\TFunc': '\mathrm{T}' '\UFunc': '\mathrm{U}' '\uFunc':
'\mathrm{u}' '\VFunc': '\mathrm{V}' '\vFunc': '\mathrm{v}' '\cPDVFunc':
'\mathbb{C}' '\pPDVFunc': '\mathbb{P}' '\uPDVFunc': '\mathbb{U}' '\cLevFunc':
'\pmb{\cFunc}' '\VLevFunc': '\pmb{\mathrm{V}}' '\vLevFunc': '\pmb{\mathrm{v}}'
'\RevFunc': '\pmb{\Pi}' '\revFunc': '\pmb{\pi}' '\WFunc': '\mathrm{W}' '\wFunc':
'\mathrm{w}' '\XFunc': '\mathrm{X}' '\xFunc': '\mathrm{x}' '\YFunc':
'\mathrm{Y}' '\yFunc': '\mathrm{y}' '\ZFunc': '\mathrm{Z}' '\zFunc':
'\mathrm{z}' '\MPC': '\kappa' '\PIHMPC': '\varkappa' '\MinMPC': '\uline{\kappa}'
'\MinMinMPC': '\underline{\kappa}' '\MaxMinMPC': '\hat{\underline{\kappa}}'
'\MaxMPC': '\bar{\kappa}' '\MaxMaxMPC': '\bar{\bar{\kappa}}' '\itc': '\zeta'
'\kPriceAfterITC': '\mathscr{P}' '\PostITC': '\cancel{\zeta}' '\pDead':
'\mathfrak{D}' '\TaxPaid': "T" '\WMid': '\BLev' '\wMid': '\bLev' '\Wmid':
'\BRat' '\wmid': '\bRat' '\Dvdnd': '\mathbf{D}' '\dvdnd': "d" '\edvdnd':
'\grave{\dvdnd}' '\hEnd': '\mathfrak{h}' '\GovSpend': "X" '\govSpend': "x"
'\xpend': '\xi' '\expend': '\xi' '\TEnd': "T" '\VEnd': '\mathfrak{V}' '\vEnd':
'\mathfrak{v}' '\WEnd': '\ALev' '\wEnd': '\aLev' '\Wend': '\ARat' '\wend':
'\aRat' '\permGroFacInd': '\pmb{\phi}' '\permShkInd': '\psi' '\tranShkInd':
'\theta' '\permLvlInd': '\mathrm{p}' '\RCpnd': '\mathbf{R}' '\Mod': '\tilde'
'\Rprod': '\mathscr{R}' '\rprod': '\mathscr{r}' '\RProd': '\mathsf{R}' '\rProd':
'\mathsf{r}' '\tranShkIndStd': '\sigma*{\tranShkInd}' '\tranShkAggStd':
'\sigma*{\tranShkAgg}' '\ShkMeanOneLogStd': '\sigma*{\ShkMeanOneLog}'
'\ShkLogZeroLogStd': '\sigma*{\cancel{\ShkMeanOneLog}}' '\PermShkStd':
'\sigma*{\PermShk}' '\TranShkStd': '\sigma*{\TranShk}' '\prud': '\eta' '\tFwd':
"n" '\aE': '\aRat^{e}' '\BE': '\BRat^{e}' '\bE': '\bRat^{e}' '\CE': '\CRat^{e}'
'\cE': '\cRat^{e}' '\Price': '\mathsf{P}' '\kPrice': '\mathsf{P}' '\Severance':
'\kappa' '\MPCE': '\MPC^{e}' '\Rfree': '\mathsf{R}' '\rfree': '\mathsf{r}'
'\TaxFree': '\cancel{\Tax}' '\Age': "Z" '\age': "z" '\Wage': '\mathsf{W}'
'\wage': '\mathsf{w}' '\bTargE': '\check{b}^{e}' '\CTargE': '\CTarg^{\null}'
'\cTargE': '\check{c}^{e}' '\kTargE': '\Target{k}^{e}' '\STargE':
'\Target{\SRat}^{\null}' '\sTargE': '\Target{\sRat}^{\null}' '\yTargE':
'\check{y}^{e}' '\ME': '\MRat^{e}' '\mE': '\mRat^{e}' '\TermTime': "T"
'\ShkMeanOne': '\Theta' '\PopE': '\mathcal{E}' '\popE': "e" '\labShare': '\nu'
'\leiShare': '\zeta' '\kapShare': '\alpha' '\riskyshare': '\varsigma' '\Retire':
'\mathbb{R}' '\WPre': "K" '\wPre': "k" '\Leisure': "Z" '\leisure': "z" '\SE':
'\SRat^{e}' '\sE': '\sRat^{e}' '\BRatE': "{B}^{e}" '\bRatE': "{b}^{e}" '\CRatE':
'\CRat^{e}' '\cRatE': '\cRat^{e}' '\DiscRate': '\vartheta' '\pDeadRate':
'\grave{\cancel{\mathsf{d}}}' '\erate': '\cancel{\mho}' '\pDieRate':
'\grave{\mathsf{d}}' '\timeRate': '\vartheta' '\saveRate': '\grave{s}' '\MRatE':
'\MRat^{e}' '\mRatE': '\mRat^{e}' '\SRatE': '\SRat^{e}' '\sRatE': '\sRat^{e}'
'\srate': '\varsigma' '\urate': '\mho' '\TaxRate': "t" '\empState': '\xi'
'\discRte': '\tau' '\DiscRte': '\vartheta' '\GroRte': '\omega' '\BalGroRte':
'\tilde' '\permGroRte': '\gamma' '\PermGroRte': '\varphi' '\PopnGroRte': '\xi'
'\APRte': '\text{\thorn}' '\GPRte': '\text{\thorn}*{\PermGroRte}' '\popRte':
'\popGro' '\RPRte': '\text{\thorn}_{\rfree}' '\deprRte': '\delta' '\Value':
'\mathrm{V}' '\VE': "{V}^{e}" '\vE': "{v}^{e}" '\Save': "S" '\save': "s"
'\RSave': '\underline{\Rfree}' '\rsave': '\underline{\rfree}' '\Abve': '\bar'
'\BLevE': '\BLev^{e}' '\bLevE': '\bLev^{e}' '\CLevE': '\CLev^{e}' '\cLevE':
'\cLev^{e}' '\mLevE': '\mLev^{e}' '\SLevE': '\SLev^{e}' '\sLevE': '\sLev^{e}'
'\Alive': '\mathcal{L}' '\cFuncAbove': '\bar{\mathrm{c}}' '\aRatBF': '\pmb{a}'
'\bRatBF': '\pmb{\mathrm{b}}' '\cRatBF': '\pmb{c}' '\mRatBF': '\pmb{\mathrm{m}}'
'\ALevBF': '\mathbf{A}' '\aLevBF': '\mathbf{a}' '\BLevBF': '\mathbf{B}'
'\bLevBF': '\mathbf{b}' '\CLevBF': '\mathbf{C}' '\cLevBF': '\mathbf{c}'
'\HLevBF': '\mathbf{H}' '\hLevBF': '\mathbf{h}' '\KLevBF': '\mathbf{K}'
'\kLevBF': '\mathbf{k}' '\LLevBF': '\mathbf{L}' '\lLevBF': '\pmb{\ell}'
'\MLevBF': '\mathbf{M}' '\mLevBF': '\mathbf{m}' '\OLevBF': '\mathbf{O}'
'\oLevBF': '\mathbf{o}' '\PLevBF': '\mathbf{P}' '\pLevBF': '\mathbf{p}'
'\SLevBF': '\mathbf{S}' '\sLevBF': '\mathbf{s}' '\vLevBF': '\mathbf{v}'
'\YLevBF': '\mathbf{Y}' '\yLevBF': '\mathbf{y}' '\ZLevBF': '\mathbf{Z}'
'\zLevBF': '\pmb{z}' '\CDF': '\mathcal{F}' '\SDF': '\MLev' '\RfreeEff':
'\bar{\Rfree}' '\CGroPF': '\Lambda' '\cGroPF': '\lambda' '\WGroPF': '\mathrm{G}'
'\MPCPPF': '\Pi' '\vBeg': '\upsilon' '\WBeg': '\KLev' '\wBeg': '\kLev' '\aAgg':
'\mathsf{A}' '\cAgg': '\pmb{C}' '\permGroFacAgg': '\Phi' '\RfreeAgg':
'\Agg{\Rfree}' '\PermShkAgg': '\Psi' '\permShkAgg': '\Psi' '\TranShkAgg':
'\Theta' '\tranShkAgg': '\Theta' '\permLvlAgg': '\mathrm{P}' '\PermLvlAgg':
'\PLvl' '\zAgg': '\pmb{Z}' '\ShkMeanOneLog': '\theta' '\mBalLog':
'\BalGroRte{m}' '\EpremLog': '\varphi' '\ShkLogZeroLog':
'\cancel{\ShkMeanOneLog}' '\pLog': "p" '\ImpG': '\Im}_{\PGro' '\impg':
'\imath}_{\pGro' '\ATarg': '\check{A}' '\aTarg': '\check{a}' '\BTarg':
'\check{B}' '\bTarg': '\check{b}' '\CTarg': '\Target{C}' '\cTarg': '\check{c}'
'\BTargTarg': '\Target{\Target{\BRat}}' '\bTargTarg': '\Target{\Target{\bRat}}'
'\cTargTarg': '\Target{\Target{\cRat}}' '\STargTarg': '\Target{\Target{\SRat}}'
'\sTargTarg': '\Target{\Target{\sRat}}' '\kTarg': '\Target{k}' '\mTarg':
'\check{m}' '\STarg': '\Target{\SRat}' '\sTarg': '\Target{\sRat}' '\vTarg':
'\Target{\vRat}' '\yTarg': '\check{y}' '\CGroOverG': '\Upsilon' '\avg': '\bar'
'\h': "h" '\Wealth': "O" '\wealth': "o" '\Hi': '\hat' '\Chi': '\mathrm{X}'
'\NI': "Z" '\TaxUI': '\tau' '\adj': '\mathrm{j}' '\PermGroFacAdj':
'\underline{\PermGroFac}' '\PGroAdj': '\underline{\PGro}' '\pGroAdj':
'\underline{\pGro}' '\PatPGroAdj': '\text{\pmb{\Thorn}}_{\underline{\PGro}}'
'\patpGroAdj': '\text{\thorn}_{\underline{\pGro}}' '\PermGroFacuAdj':
'\underline{\underline{\PermGroFac}}' '\PGrouAdj':
'\underline{\underline{\PGro}}' '\pGrouAdj': '\underline{\underline{\pGro}}'
'\DiscAltuAdj': '\underline{\underline{\beth}}' '\TEndBak': '\mathsf{p}'
'\tBak': '\pmb{n}' '\TEatBak': '\mathtt{q}' '\ek': '\lambda' '\Shk': '\Phi'
'\shk': '\phi' '\PermShk': '\mathbf{\Psi}' '\permShk': '\psi' '\uInvEuPermShk':
'\underline{\underline{\PermShk}}' '\PShk': '\Psi' '\pShk': '\psi' '\pshk':
'\psi' '\TShk': '\Xi' '\tShk': '\xi' '\tshk': '\xi' '\Work': '\mathbb{W}' '\vk':
'\lambda' '\util': "u" '\TranShkAll': '\pmb{\xi}' '\tShkAll': '\xi' '\WAll': "O"
'\wAll': "o" '\Lvl': '\mathbf' '\ALvl': '\mathbf{A}' '\aLvl': '\mathbf{a}'
'\BLvl': '\mathbf{B}' '\bLvl': '\mathbf{b}' '\CLvl': '\mathbf{C}' '\cLvl':
'\mathbf{c}' '\DLvl': '\mathbf{D}' '\dLvl': '\mathbf{d}' '\ELvl': '\mathbf{E}'
'\eLvl': '\mathbf{e}' '\FLvl': '\mathbf{F}' '\fLvl': '\mathbf{f}' '\GLvl':
'\mathbf{G}' '\HLvl': '\mathbf{H}' '\hLvl': '\mathbf{h}' '\ILvl': '\mathbf{I}'
'\iLvl': '\mathbf{i}' '\JLvl': '\mathbf{J}' '\jLvl': '\mathbf{j}' '\KLvl':
'\mathbf{K}' '\kLvl': '\mathbf{k}' '\LLvl': '\mathbf{L}' '\ABalLvl':
'\BalGroFac{\ALvl}' '\MBalLvl': '\BalGroFac{\MNrm}' '\mBalLvl': '\BalGroFac{m}'
'\MLvl': '\mathbf{M}' '\mLvl': '\mathbf{m}' '\PermLvl': '\pLvl' '\NLvl':
'\mathbf{N}' '\PopnLvl': '\pmb{\mathrm{N}}' '\OLvl': '\mathbf{O}' '\PLvl':
'\mathbf{P}' '\pLvl': '\mathbf{p}' '\QLvl': '\mathbf{Q}' '\RLvl': '\mathbf{R}'
'\rLvl': '\mathbf{r}' '\SLvl': '\mathbf{S}' '\sLvl': '\mathbf{s}' '\TLvl':
'\mathbf{T}' '\ULvl': '\mathbf{U}' '\VLvl': '\mathbf{V}' '\vLvl': '\mathbf{v}'
'\WLvl': '\mathbf{W}' '\XLvl': '\mathbf{X}' '\YLvl': '\mathbf{Y}' '\yLvl':
'\mathbf{y}' '\ZLvl': '\mathbf{Z}' '\zLvl': '\mathbf{z}' '\Ham': '\mathcal{H}'
'\EPrem': '\Phi' '\eprem': '\varphi' '\tHorOfm': '\pmb{n}' '\debtLim':
'\mathsf{d}' '\tTerm': "T" '\vFirm': '\mathrm{e}' '\ANrm': "A" '\aNrm': "a"
'\BNrm': "B" '\bNrm': "b" '\CNrm': "C" '\cNrm': "c" '\GPFacNrm':
'\APFac_{\PermGroFacAdj}' '\DNrm': "D" '\dNrm': "d" '\ENrm': "E" '\eNrm': "e"
'\FNrm': "F" '\fNrm': "f" '\bTrgNrm': '\TargetNrm{\bNrm}' '\mTrgNrm':
'\TargetNrm{m}' '\HNrm': "H" '\hNrm': "h" '\INrm': "I" '\iNrm': "i" '\JNrm': "J"
'\jNrm': "j" '\KNrm': "K" '\kNrm': "k" '\MNrm': "M" '\mNrm': "m" '\PNrm': "P"
'\pNrm': "p" '\RNrm': '\mathcal{R}' '\rNrm': "s" '\SNrm': "S" '\sNrm': "s"
'\TargetNrm': '\hat' '\VNrm': "V" '\vNrm': "v" '\xNrm': "x" '\YNrm': "Y"
'\yNrm': "y" '\ZNrm': "Z" '\zNrm': "z" '\Rnorm': '\mathcal{R}' '\rnorm':
'\mathit{r}' '\vNorm': '\mathrm{w}' '\WHum': '\HLev' '\wHum': '\hLev' '\Whum':
'\HRat' '\whum': '\hRat' '\Num': "N" '\VNum': "V" '\vNum': "v" '\Mean':
'\mathbb{M}' '\tThen': '\tau' '\valfn': '\mathrm{v}' '\aMin':
'\underline{\aRat}' '\bMin': '\underline{\bRat}' '\MPCmin': '\uline{\kappa}'
'\hEndMin': '\underline{\mathfrak{h}}' '\aboveMin': '\blacktriangle' '\hMin':
'\underline{\h}' '\HMin': '\underline{H}' '\pShkMin': '\underline{\psi}'
'\whumMin': '\underline{\hRat}' '\MPCminmin': '\underline{\kappa}'
'\TranShkEmpMin': '\underline{\TranShkEmp}' '\tranShkEmpMin':
'\underline{\tranShkEmp}' '\tShkEmpMin': '\underline{\theta}' '\MPSmin':
'\pZero^{1/\CRRA} \RPFac' '\MPCmaxmin': '\hat{\underline{\kappa}}' '\Decision':
'\mathbb{D}' '\SeveranceRatio': '\varsigma' '\Lo': '\check' '\ShkLogZero':
'\cancel{\ShkMeanOne}' '\pZero': '\wp' '\pNotZero': '(1-\pZero)' '\LGro':
'\Lambda' '\lGro': '\lambda' '\PGro': '\Gamma' '\pGro': '\gamma' '\GDPGro':
'\gimel' '\EmpGro': '\Xi' '\empGro': '\xi' '\PopGro': '\Xi' '\popGro': '\xi'
'\PatPGro': '\text{\pmb{\Thorn}}_{\PGro}' '\patpGro': '\text{\thorn}_{\pGro}'
'\XperGro': '\mathsf{X}' '\xperGro': '\mathsf{x}' '\DivGro': '\mathrm{G}'
'\divGro': '\mathsf{g}' '\WGro': '\mathrm{G}' '\wGro': '\mathsf{g}'
'\RnormWGro': '\mathcal{R}_{\WGro}' '\rnormwGro': '\mathit{r}_{\wGro}'
'\PatWGro': '\text{\pmb{\Thorn}}_{\WGro}' '\patwGro': '\text{\thorn}_{\wGro}'
'\PtyGro': '\Phi' '\ptyGro': '\phi' '\RBoro': '\bar{\Rfree}' '\rboro':
'\bar{\rfree}' '\Pareto': '\zeta' '\Kap': "K" '\kap': "k" '\EEndMap':
'\mathsf{E}' '\TMap': '\mathscr{T}' '\cP': '\cons^{\prime}' '\MPCP': '\pi'
'\taxDep': '\partial' '\FP': '\mathrm{F}^{\prime}' '\fP': '\mathrm{f}^{\prime}'
'\TranShkEmp': '\pmb{\xi}' '\tranShkEmp': '\xi' '\TShkEmp': '\Theta' '\tShkEmp':
'\theta' '\TranShk': '\Theta' '\tranShk': '\theta' '\IncUnemp': '\mu' '\Pop':
"L" '\cPP': '\cons^{\prime\prime}' '\FPP': '\mathrm{F}^{\prime\prime}' '\fPP':
'\mathrm{f}^{\prime\prime}' '\cPPP': '\cons^{\prime\prime\prime}' '\uPPP':
'\mathrm{u}^{\prime\prime\prime}' '\uPP': '\mathrm{u}^{\prime\prime}'
'\TaxCorp': '\Large \tau' '\taxCorp': '\tau' '\uP': '\mathrm{u}^{\prime}' '\q':
'\koppa' '\adjPar': '\omega' '\tranShkIndVar': '\sigma^{2}_{\tranShkInd}'
'\tranShkAggVar': '\sigma^{2}_{\tranShkAgg}' '\ShkMeanOneLogVar':
'\sigma^{2}_{\ShkMeanOneLog}' '\ShkLogZeroLogVar':
'\sigma_{\cancel{\ShkMeanOneLog}}^{2}' '\PermShkVar': '\sigma^{2}_{\PermShk}'
'\TranShkVar': '\sigma^{2}_{\TranShk}' '\sdr': '\mRat' '\Estdr':
'\sigma*{\risky}' '\xFer': '\chi' '\XFer': "X" '\nIter': "n" '\power': '\eta'
'\labor': '\ell' '\Labor': '\mathrm{L}' '\PLabor': "P" '\Plabor': "P" '\tHor':
'\mathsf{n}' '\error': '\epsilon' '\Depr': '\daleth' '\depr': '\delta' '\ImpR':
'\Im}*{\Rfree' '\impr': '\imath}_{\rfree' '\EVarr': '\sigma_{\Risky}^{2}'
'\Evarr': '\sigma*{\risky}^{2}' '\Err': "Z" '\err': "z" '\CGroOverR': '\Phi'
'\corr': '\varrho' '\curr': "1" '\Curr': "t" '\tCurr': "t" '\PatR':
'\text{\pmb{\Thorn}}*{\Rfree}' '\patr': '\text{\thorn}_{\rfree}' '\PDies':
'\mathsf{D}' '\pDies': '\mathsf{d}' '\PLives': '\cancel{\PDies}' '\pLives':
'\cancel{\pDies}' '\Stocks': "S" '\stocks': "s" '\TaxNetTrans': "Z"
'\taxNetTrans': "z" '\unins': '\zeta' '\Cons': "C" '\cons': "c" '\MPS':
'\lambda' '\MinMPS': '\pZero^{1/\CRRA} \PatR' '\MaxMPS': '\PatR' '\CGroPS':
'\chi' '\Hours': '\mathfrak{H}' '\hours': '\mathfrak{h}' '\ASS': "A" '\aSS': "a"
'\cEss': "{c}^{e}" '\mEss': '\check{m}^{e}' '\vEss': '\check{v}^{e}' '\MSS':
'\breve{M}' '\mSS': '\breve{m}' '\RGross': '\breve{\mathsf{R}}' '\rGross':
'\breve{\mathsf{r}}' '\tSS': "t" '\effUnits': "X" '\Surplus': "Z" '\surplus':
"z" '\TEat': '\TEnd' '\patpGrohat': '\hat{\text{\thorn}}_{\pGro}' '\aMat':
'[\mathrm{a}]' '\bMat': '[\mathrm{\bNrm}]' '\cMat': '[\mathrm{\cNrm}]'
'\tShkMat': '[\mathrm{\tShkEmp}]' '\mMat': '[\mathrm{m}]' '\xMat':
'[\mathrm{\xNrm}]' '\yMat': '[\mathrm{\yNrm}]' '\Pat': '\text{\pmb{\Thorn}}'
'\pat': '\text{\thorn}' '\ARat': "A" '\aRat': "a" '\NFARat': '\NRat' '\BRat':
"B" '\bRat': "b" '\CRat': "C" '\cRat': "c" '\ccRat': '\mathsf{c}' '\dRat': "d"
'\WEndRat': '\ARat' '\wEndRat': '\aRat' '\HRat': "H" '\hRat': "h" '\IRat': "I"
'\iRat': "i" '\KRat': "K" '\kRat': "k" '\LRat': "L" '\lRat': "l" '\WAllRat': "O"
'\wAllRat': "o" '\MRat': "M" '\mRat': "m" '\NRat': "N" '\nRat': "n" '\ORat': "O"
'\oRat': "o" '\pRat': "p" '\GDPRat': "P" '\gdpRat': "p" '\SRat': "S" '\sRat':
"s" '\VRat': "V" '\vRat': "v" '\WRat': "O" '\wRat': "o" '\XRat': "X" '\xRat':
"x" '\YRat': "Y" '\yRat': "y" '\ZRat': "Z" '\zRat': "z" '\Debt': "D" '\debt':
"d" '\Target': '\check' '\WNet': "X" '\wNet': "x" '\straight': '\Pi' '\weight':
'\omega' '\Habit': "H" '\habit': "h" '\WMkt': '\MLev' '\wMkt': '\mLev' '\wmkt':
'\mLev' '\Alt': '\grave' '\DiscFacAlt': '\beth' '\DiscAlt': '\beth' '\ValAlt':
'\mathcal{V}' '\vOptAlt': '\grave{\tilde{\mathfrak{v}}}' '\RiskyAlt':
'\pmb{\mathfrak{R}}' '\riskyAlt': '\pmb{\mathfrak{r}}' '\uPmt': '\mu'
'\SeverancePayment': '\mathcal{S}' '\kapRent': '\varkappa' '\Discount': '\beta'
'\tinyAmount': '\epsilon' '\WTot': '\mathbf{O}' '\wTot': '\mathbf{o}' '\Wtot':
"O" '\wtot': "o" '\vOpt': '\tilde{\mathfrak{v}}' '\Rport': '\mathbb{R}'
'\rport': '\mathbb{r}' '\FDist': '\mathcal{F}' '\fDist': '\mathcal{f}' '\Next':
"t+1" '\tNext': "t+1" '\BU': "{B}^{u}" '\bU': "{b}^{u}" '\CU': '\CRat^{u}'
'\cU': '\cRat^{u}' '\MPCU': '\MPC^{u}' '\MU': "{M}^{u}" '\mU': "{m}^{u}"
'\PopU': '\mathcal{U}' '\SU': '\SRat^{u}' '\sU': '\sRat^{u}' '\PatU':
'\text{\pmb{\Thorn}}_{\urate}' '\patu': '\text{\thorn}_{\urate}' '\bRatU':
"{b}^{u}" '\CRatU': '\CRat^{u}' '\cRatU': '\cRat^{u}' '\SRatU': '\SRat^{u}'
'\sRatU': '\sRat^{u}' '\VU': "{V}^{u}" '\vU': "{v}^{u}" '\BLevU': '\BLev^{u}'
'\bLevU': '\bLev^{u}' '\CLevU': '\CLev^{u}' '\cLevU': '\cLev^{u}' '\SLevU':
'\SLev^{u}' '\sLevU': '\sLev^{u}' '\pSav': '\phi' '\PDV': '\mathbb{P}' '\CPDV':
'\text{PDV($C$)}' '\PPDV': '\text{PDV($P$)}' '\ALev': "A" '\aLev': "a"
'\NFALev': '\NLev' '\BLev': "B" '\bLev': "b" '\CLev': "C" '\cLev': "c" '\DLev':
"D" '\ELev': "E" '\FLev': "F" '\fLev': "f" '\GLev': "G" '\HLev': '\pmb{H}'
'\hLev': '\pmb{h}' '\ILev': "I" '\iLev': "i" '\JLev': "J" '\KLev': "K" '\kLev':
"k" '\lLev': '\ell' '\LLev': "L" '\WAllLev': '\mathbf{O}' '\wAllLev':
'\mathbf{o}' '\MLev': "M" '\mLev': "m" '\NLev': "N" '\nLev': "n" '\oLev':
'\pmb{o}' '\OLev': "O" '\pLev': '\pmb{p}' '\PLev': "P" '\GDPLev': '\pmb{P}'
'\gdpLev': '\pmb{p}' '\PopLev': '\pmb{N}' '\QLev': "Q" '\RLev': "R" '\SLev': "S"
'\sLev': "s" '\TLev': "T" '\ULev': "U" '\uLev': "u" '\VLev': "V" '\vLev': "v"
'\wLev': '\pmb{w}' '\WLev': "W" '\XLev': "X" '\xLev': "x" '\TaxLev': "T"
'\YLev': "Y" '\yLev': "y" '\PtyLev': "A" '\ptyLev': "a" '\ZLev': "Z" '\zLev':
"z" '\Rev': '\Pi' '\rev': '\pi' '\tPrev': "t-1" '\Div': "D" '\DiscFacLiv':
'\underline{\DiscFacRaw}' '\Inv': "I" '\inv': "i" '\TaxCombInv':
'\mathcal{T}^{-1}' '\EPermShkInv': '\Ex[\PermShk^{-1}]' '\InvEPermShkInv':
'\underline{\PermShk}' '\EpShkInv': '\Ex[\pShk^{-1}]' '\InvEpShkInv':
'\underline{\psi}' '\uInvEpShkuInv': '\underline{\underline{\psi}}' '\VInv':
'\Lambda' '\vInv': '\scriptstyle \Lambda \displaystyle' '\cov': '\textup{cov}'
'\DiscFacRaw': '\beta' '\GPFacRaw': '\APFac\_{\PermGroFac}' '\Belw': '\ushort'
'\GovNW': "N" '\govNW': "n" '\cFuncBelow': '\uline{\mathrm{c}}' '\tNow': "t"
'\cFuncMax': '\bar{\bar{\mathrm{c}}}' '\MPCmax': '\bar{\kappa}' '\MPSmax':
'\RPFac' '\MPCmaxmax': '\bar{\bar{\kappa}}' '\Tax': '\tau' '\tax': '\tau' '\Ex':
'\mathbb{E}' '\prudEx': '\omega' '\Steady': '\bar' '\Risky': '\mathbf{R}'
'\risky': '\mathbf{r}' '\Seniority': '\mathsf{X}' '\seniority': '\mathsf{x}'
'\wealthShare': '\delta'

---

<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": "slide"} -->

# Understanding the Distribution of Wealth and the Racial Wealth Gap using Data Science

## By Alan Lujan, PhD

## JHU Economics, Econ-ARK

<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": "slide"} -->

![](../figures/total_net_worth_per_decile.svg)

<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": "slide"} -->

![](../figures/total_net_worth_per_centile.svg)

<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": "slide"} -->

## Distribution of Wealth in the US

- Highly unequal
- Top 1% owns almost 40% of the wealth
- Bottom 50% owns less than 2% of the wealth
- Racial wealth gap is large and persistent

<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": "slide"} -->

## Survey of Consumer Finances

- Conducted by the Federal Reserve
- Every 3 years
- Wealth, income, and demographic data
- Publicly available (some variables are private)

Let's take a look:
[https://www.federalreserve.gov/econres/scfindex.htm](https://www.federalreserve.gov/econres/scfindex.htm)

<!-- #endregion -->

```python editable=true slideshow={"slide_type": "slide"}
import warnings
import matplotlib.pyplot as plt  # for plotting
import pandas as pd  # for data manipulation
import numpy as np  # for numerical computation
import seaborn as sns  # for plotting
from statsmodels.stats.weightstats import DescrStatsW  # for weighted statistics
from utilities import (
    tens_of_thousands_formater,
    hundreds_of_thousands_formater,
    millions_formater,
    trillions_formater,
)
from IPython.display import display, HTML


warnings.simplefilter(action="ignore", category=FutureWarning)
warnings.simplefilter(action="ignore", category=DeprecationWarning)
sns.set_theme(context="talk", style="whitegrid", palette="colorblind")
```

```python editable=true slideshow={"slide_type": "slide"}
scf_data = pd.read_stata("../data/scf_processed.dta")
display(HTML(scf_data.sample(5).T.to_html(max_rows=None)))
```

<!-- #region editable=true slideshow={"slide_type": "slide"} -->

# The Distribution of Wealth in the US

<!-- #endregion -->

```python editable=true slideshow={"slide_type": "slide"}
key_var = "networth"
scf_data["totalwealth"] = scf_data[key_var] * scf_data["wgt"]

# Add noise to totalwealth to avoid ties
np.random.default_rng()
eps = np.random.uniform(-0.01, 0.01, len(scf_data))
scf_data["totalwealth_eps"] = scf_data["totalwealth"] + eps

scf_2022 = scf_data[scf_data.year == "2022"]
# # sort values by total_wealth
scf_2022 = scf_2022.sort_values("totalwealth", ascending=False)

# Assign deciles based on the sorted total_wealth
scf_2022["decile"] = pd.qcut(scf_2022["totalwealth_eps"], 10, labels=False)
scf_2022["percentile"] = pd.qcut(scf_2022["totalwealth_eps"], 100, labels=False)

q = [0, 0.5, 0.8, 0.9, 0.95, 0.99, 0.995, 0.999, 1]
scf_2022["quantile"] = pd.qcut(scf_2022["totalwealth_eps"], q, labels=q[:-1])

# Calculate Total Net Worth per wealth decile, percentile, income decile and income percentile
total_wealth_per_decile = scf_2022.groupby("decile")["totalwealth"].sum()
total_wealth_per_centile = scf_2022.groupby("percentile")["totalwealth"].sum()
total_wealth_per_quantile = scf_2022.groupby("quantile")["totalwealth"].sum()
```

```python editable=true jupyterlab-deck={"layer": null} slideshow={"slide_type": "slide"}
# Create a barplot
plt.figure(figsize=(12, 6))

sns.barplot(
    x=total_wealth_per_decile.index,
    y=total_wealth_per_decile.values,
)

# Set labels and title
plt.xlabel("Deciles")
plt.ylabel("Total Net Worth (in trillions of USD)")
plt.title("Distribution of Wealth by Deciles")
# plt.yscale("log")

# Format y axis
plt.gca().yaxis.set_major_formatter(trillions_formater)

plt.savefig("../figures/total_net_worth_per_decile.svg")
# Show the plot
plt.show()
```

```python editable=true slideshow={"slide_type": "slide"}
# Create a barplot
plt.figure(figsize=(12, 6))

bar_plot = sns.barplot(
    x=total_wealth_per_centile.index,
    y=total_wealth_per_centile.values,
)

# Set labels and title
plt.xlabel("Percentiles")
plt.ylabel("Total Net Worth (in trillion of dollars)")
plt.title("Distribution of Wealth by Percentiles")

# Format y axis
plt.gca().yaxis.set_major_formatter(trillions_formater)

# Modify x-axis to show 100th percentile down to 1st percentile
x_ticks = np.arange(0, 100, 10)
x_ticks = np.append(x_ticks, 99)
plt.xticks(x_ticks, total_wealth_per_centile.index[x_ticks])
# plt.yscale("log")

plt.savefig("../figures/total_net_worth_per_centile.svg")
# Show the plot
plt.show()
```

```python editable=true jupyterlab-deck={"layer": null} slideshow={"slide_type": "slide"}
# Create a barplot
plt.figure(figsize=(12, 6))

sns.barplot(
    x=total_wealth_per_quantile.index,
    y=total_wealth_per_quantile.values,
)

# Set labels and title
plt.xlabel("Quantiles")
plt.ylabel("Total Net Worth (in trillions of USD)")
plt.title("Distribution of Wealth by Quantiles")
# plt.yscale("log")

# Format y axis
plt.gca().yaxis.set_major_formatter(trillions_formater)

# Assuming q and total_wealth_per_quantile.index are defined
x_ticks = [f"{q[i]*100} - {q[i+1]*100}" for i in range(len(q) - 1)]
plt.xticks(range(len(x_ticks)), x_ticks)

# Rotate x-labels
plt.xticks(rotation=45)


plt.savefig("../figures/total_net_worth_per_quantile.svg")
# Show the plot
plt.show()
```

```python editable=true slideshow={"slide_type": "slide"}
total_wealth_per_inc_decile = scf_2022.groupby("inccat")["totalwealth"].sum()  # decile


inc_cat_lbl = {
    1: "0-20",
    2: "20-39.9",
    3: "40-59.9",
    4: "60-79.9",
    5: "80-89.9",
    6: "90-100",
}  # income categories

# Create a barplot
plt.figure(figsize=(12, 6))


barplot = sns.barplot(
    x=total_wealth_per_inc_decile.index,
    y=total_wealth_per_inc_decile.values,
)

# Apply inc_cat_lbl to the x labels
barplot.set_xticklabels([inc_cat_lbl[i] for i in total_wealth_per_inc_decile.index])

# Set labels and title
plt.xlabel("Income Deciles")
plt.ylabel("Total Net Worth (in trillions of dollars)")
plt.title("Distribution of Wealth by Income Deciles")

# Format y axis
plt.gca().yaxis.set_major_formatter(trillions_formater)

plt.show()
```

```python editable=true slideshow={"slide_type": "slide"}
total_wealth_per_inc_percentile = scf_2022.groupby("incpctlecat")[
    "totalwealth"
].sum()  # percentile

inc_pct_lbl = {
    1: "0-9.9",
    2: "10-19.9",
    3: "20-29.9",
    4: "30-39.9",
    5: "40-49.9",
    6: "50-59.9",
    7: "60-69.9",
    8: "70-79.9",
    9: "80-89.9",
    10: "90-94.9",
    11: "95-98.9",
    12: "99-100",
}

# Create a barplot
plt.figure(figsize=(12, 6))


barplot = sns.barplot(
    x=total_wealth_per_inc_percentile.index,
    y=total_wealth_per_inc_percentile.values,
)

# Apply inc_cat_lbl to the x labels
barplot.set_xticklabels([inc_pct_lbl[i] for i in total_wealth_per_inc_percentile.index])

# Format y axis
plt.gca().yaxis.set_major_formatter(trillions_formater)

# Rotate x-labels
plt.xticks(rotation=45)


# Set labels and title
plt.xlabel("Percentiles")
plt.ylabel("Total Net Worth (in trillions of dollars)")
plt.title("Distribution of Wealth by Income Percentiles")

plt.show()
```

<!-- #region editable=true slideshow={"slide_type": "slide"} -->

# The Racial Wealth Gap

<!-- #endregion -->

```python editable=true slideshow={"slide_type": "slide"}
# Calculate weighted mean
average_wealth_by_race = scf_2022.groupby("racecl4_lbl").apply(
    lambda x: np.average(x[key_var], weights=x["wgt"])
)
```

```python editable=true slideshow={"slide_type": "slide"}
# Create a barplot
plt.figure(figsize=(12, 6))
sns.barplot(x=average_wealth_by_race.index, y=average_wealth_by_race.values)

plt.gca().yaxis.set_major_formatter(millions_formater)

# Rotate x-labels
plt.xticks(rotation=10)

plt.show()
```

```python editable=true slideshow={"slide_type": "slide"}
# Calculate weighted median
def weighted_median(df, median_col, weight_col):
    return DescrStatsW(df[median_col], weights=df[weight_col]).quantile(
        0.5, return_pandas=False
    )[0]


median_wealth_by_race = scf_2022.groupby("racecl4_lbl").apply(
    weighted_median, key_var, "wgt"
)
```

```python editable=true slideshow={"slide_type": "slide"}
# Create a barplot

plt.figure(figsize=(12, 6))
sns.barplot(x=median_wealth_by_race.index, y=median_wealth_by_race.values)

# Format y-axis labels
plt.gca().yaxis.set_major_formatter(hundreds_of_thousands_formater)

# Rotate x-labels
plt.xticks(rotation=10)

plt.show()
```

<!-- #region editable=true slideshow={"slide_type": "slide"} -->

# Inequality Over Time

<!-- #endregion -->

```python editable=true slideshow={"slide_type": "slide"}
# sort values by total_wealth

scf_data = scf_data.sort_values("totalwealth", ascending=False)

# Assign deciles based on the sorted total_wealth
scf_data["decile"] = scf_data.groupby("year")["totalwealth_eps"].transform(
    lambda x: pd.qcut(x, 10, labels=False)
)
scf_data["percentile"] = scf_data.groupby("year")["totalwealth_eps"].transform(
    lambda x: pd.qcut(x, 100, labels=False)
)
scf_data["quantile"] = scf_data.groupby("year")["totalwealth_eps"].transform(
    lambda x: pd.qcut(x, q, labels=False)
)

# Calculate Total Net Worth per wealth decile, percentile, income decile and income percentile
total_wealth_per_decile_year = (
    scf_data.groupby(["decile", "year"])["totalwealth"].sum().reset_index()
)
total_wealth_per_centile_year = (
    scf_data.groupby(["percentile", "year"])["totalwealth"].sum().reset_index()
)
total_wealth_per_quantile_year = (
    scf_data.groupby(["quantile", "year"])["totalwealth"].sum().reset_index()
)
total_wealth_per_inc_decile_year = (
    scf_data.groupby(["inccat", "year"])["totalwealth"].sum().reset_index()
)
total_wealth_per_inc_percentile_year = (
    scf_data.groupby(["incpctlecat", "year"])["totalwealth"].sum().reset_index()
)
```

```python editable=true slideshow={"slide_type": "slide"}
plt.figure(figsize=(12, 6))

sns.lineplot(x="year", y="totalwealth", hue="decile", data=total_wealth_per_decile_year)

plt.xticks(rotation=45)
plt.show()
```

```python editable=true slideshow={"slide_type": "slide"}
plt.figure(figsize=(12, 6))


sns.lineplot(
    x="year", y="totalwealth", hue="inccat", data=total_wealth_per_inc_decile_year
)

plt.xticks(rotation=45)
plt.show()
```

```python editable=true slideshow={"slide_type": "slide"}
plt.figure(figsize=(12, 6))


sns.lineplot(
    x="year",
    y="totalwealth",
    hue="incpctlecat",
    data=total_wealth_per_inc_percentile_year,
)

plt.xticks(rotation=45)
plt.show()
```

<!-- #region editable=true slideshow={"slide_type": "slide"} -->

# The Evolution of the Racial Wealth Gap

<!-- #endregion -->

```python editable=true slideshow={"slide_type": "slide"}
# Filter out 'Other or Multiple race'
filtered_data = scf_data[scf_data["racecl4_lbl"] != "Other or Multiple race"]

# Calculate median wealth by race
median_wealth_by_race = (
    filtered_data.groupby(["racecl4_lbl", "year"])
    .apply(weighted_median, key_var, "wgt")
    .reset_index()
)

plt.figure(figsize=(12, 6))


# Create line plot
sns.lineplot(x="year", y=0, hue="racecl4_lbl", data=median_wealth_by_race)

# Rotate x-axis labels
plt.xticks(rotation=45)

# Move the legend below the plot and make it horizontal
plt.legend(bbox_to_anchor=(0.5, -0.3), loc="upper center", ncol=3)
```

```python editable=true slideshow={"slide_type": "slide"}
filtered_df = scf_data[
    (scf_data["racecl4_lbl"] != "Other or Multiple race")
    & scf_data["age"].between(21, 80)
    & scf_data["networth"]
]
```

```python editable=true slideshow={"slide_type": "fragment"}
def weighted_mean_median(group):
    year = group["age_lbl"].iloc[0]
    race_lbl = group["race_lbl"].iloc[0]
    weights = group["wgt"]

    stats_net_worth = DescrStatsW(group["networth"], weights=weights)
    stats_fin = DescrStatsW(group["fin"], weights=weights)
    stats_finincome = DescrStatsW(group["finincome"], weights=weights)

    return pd.DataFrame(
        {
            "age_lbl": year,
            "race_lbl": race_lbl,
            "networth_mean": stats_net_worth.mean,
            "networth_median": stats_net_worth.quantile(0.5),
            "fin_mean": stats_fin.mean,
            "fin_median": stats_fin.quantile(0.5),
            "finincome_mean": stats_finincome.mean,
            "finincome_median": stats_finincome.quantile(0.5),
        }
    )


grouped_df = filtered_df.groupby(["age_lbl", "race_lbl"]).apply(weighted_mean_median)
```

```python editable=true slideshow={"slide_type": "slide"}
# Create a figure
plt.figure(figsize=(12, 6))

# Create a line graph
line_plot = sns.lineplot(
    x="age_lbl",
    y="networth_median",
    hue="race_lbl",
    style="race_lbl",
    data=grouped_df,
    linewidth=3,
)

# Set title and labels
plt.title("Net Worth (in $100,000s)")
plt.xlabel("age_lbl")
plt.ylabel("Net Worth")

# Rotate x-tick labels
plt.xticks(rotation=45)

# Format y-axis in hundreds of thousands

plt.gca().yaxis.set_major_formatter(hundreds_of_thousands_formater)

# Move the legend below the plot and make it horizontal
plt.legend(bbox_to_anchor=(0.5, -0.3), loc="upper center", ncol=3)

plt.show()
```

```python editable=true slideshow={"slide_type": "slide"}
# Create a figure
plt.figure(figsize=(12, 6))

# Create a line graph
line_plot = sns.lineplot(
    x="age_lbl",
    y="fin_median",
    hue="race_lbl",
    style="race_lbl",
    data=grouped_df,
    linewidth=3,
)


# Set title and labels
plt.title("Financial Wealth (in $10,000s)")
plt.xlabel("age_lbl")
plt.ylabel("Financial Wealth")

# Rotate x-tick labels
plt.xticks(rotation=45)

plt.gca().yaxis.set_major_formatter(tens_of_thousands_formater)

# Move the legend below the plot and make it horizontal
plt.legend(bbox_to_anchor=(0.5, -0.30), loc="upper center", ncol=3)

plt.show()
```

<!-- #region editable=true slideshow={"slide_type": "slide"} -->

# The Racial Stock Market Participation Gap

<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": "slide"} -->

![](equity_year.svg)

<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": "slide"} -->

![](equity_age.svg)

<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": "slide"} -->

# Quantitative/Structural Economics

\begin{equation} \vFunc*{t}(\pLvl*{t},\mLvl*{t}) = \max*{\{\cFunc,
\riskyshare\}_{t}^{T}} ~ \uFunc(\cLvl_{t})+\Ex*{t}\left[\sum*{n=1}^{T-t}
{\beth}^{n} \Alive*{t}^{t+n}\hat{\DiscFac}*{t}^{t+n} \uFunc(\cLvl\_{t+n})
\right] \label{eq:life-cyclemax} \end{equation}

where $\pLvl_{t}$ is the permanent income level, $\mLvl_{t}$ is total market
resources, $\cLvl_{t}$ is consumption, and

\begin{align} \beth & : \text{time-invariant `pure' discount factor} \\
\Alive*{t}^{t+n} & : \text{probability to }\Alive\text{ive until age $t+n$ given
alive at age $t$} \\ \hat{\DiscFac}*{t}^{t+n} & : \text{age-varying discount
factor between ages $t$ and $t+n$.} \end{align}

<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": "slide"} -->

\begin{align} {\vFunc}_{t}({m}_{t}) & = \max*{\{\cNrm*{t}, \riskyshare*{t}\}} ~
\uFunc(\cNrm*{t})+\beth\Alive*{t+1}\hat{\DiscFac}*{t+1}
\Ex*{t}[(\pShk*{t+1}\permGroFac*{t+1})^{1-\CRRA}{\vFunc}*{t+1}({m}_{t+1})] \\ &
\text{s.t.} & \\ \aNrm_{t} & = {m}_{t}-\cNrm_{t} \\ \Rport*{t+1} & = \Rfree +
(\Risky*{t+1}-\Rfree)\riskyshare*{t} \\ {m}*{t+1} & =
\aNrm*{t}\underbrace{\left(\frac{\Rport*{t+1}}{\pShk*{t+1}\permGroFac*{t+1}}\right)}_{\equiv
\RNrm_{t+1}} + ~\tShkEmp\_{t+1} \end{align}

\begin{align} \pShk*{t+1} & : \text{mean-one shock to permanent income} \\
\permGroFac*{t+1} & : \text{permanent income growth factor} \\ \TranShkEmp*{t+1}
& : \text{transitory shock to permanent income} \\ \Risky*{t+1} & : \text{risky
asset return factor} \\ \Rport*{t+1} & : \text{portfolio return factor} \\
\RNrm*{t+1} & : \text{permanent income growth normalized return factor}
\end{align}{align}{align}

<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": "slide"} -->

# Econ-ARK

How do we solve these models?

- with computers...

Check out Econ-ARK [https://econ-ark.org/](https://econ-ark.org/)

- open source
- cutting edge
- collaborative

<!-- #endregion -->

```python editable=true slideshow={"slide_type": "slide"}
from HARK.ConsumptionSaving.ConsIndShockModel import (
    IndShockConsumerType,
    init_lifecycle,
)
from HARK.ConsumptionSaving.ConsPortfolioModel import PortfolioConsumerType

from HARK.utilities import plot_funcs
```

```python editable=true slideshow={"slide_type": "fragment"}
cons_agent = IndShockConsumerType(**init_lifecycle)
cons_agent.solve()

cons_agent.track_vars = ["aNrm", "cNrm", "pLvl", "t_age", "mNrm"]

cons_agent.T_sim = cons_agent.T_cycle
cons_agent.initialize_sim()
cons_data = cons_agent.simulate()
```

```python editable=true slideshow={"slide_type": "slide"}
plot_funcs([sol.cFunc for sol in cons_agent.solution[:40]], 0, 5)
```

```python editable=true slideshow={"slide_type": "slide"}
cons_df = pd.DataFrame(
    {
        "Age": cons_data["t_age"].flatten() + 25 - 1,
        "pIncome": cons_data["pLvl"].flatten(),
        "nrmM": cons_data["mNrm"].flatten(),
        "nrmC": cons_data["cNrm"].flatten(),
    }
)
cons_df["Cons"] = cons_df.nrmC * cons_df.pIncome
cons_df["M"] = cons_df.nrmM * cons_df.pIncome
```

```python editable=true slideshow={"slide_type": "slide"}
# Find the mean of each variable at every age
AgeMeans = cons_df.groupby(["Age"]).median().reset_index()

# Create a figure and axis
fig, ax = plt.subplots()

sns.lineplot(x=AgeMeans.Age, y=AgeMeans.pIncome, label="Permanent Income", ax=ax)
sns.lineplot(x=AgeMeans.Age, y=AgeMeans.M, label="Market resources", ax=ax)
sns.lineplot(x=AgeMeans.Age, y=AgeMeans.Cons, label="Consumption", ax=ax)

# Set labels and title
ax.set_xlabel("Age")
ax.set_ylabel("Thousands of USD")
ax.set_title("Variable Medians Conditional on Survival")


# Show legend
ax.legend()

plt.show()
```

```python editable=true slideshow={"slide_type": "slide"}
port_agent = PortfolioConsumerType(**init_lifecycle)
port_agent.solve()

port_agent.track_vars = ["aNrm", "cNrm", "pLvl", "t_age", "mNrm"]

port_agent.T_sim = port_agent.T_cycle
port_agent.initialize_sim()
port_data = port_agent.simulate()
```

```python editable=true slideshow={"slide_type": "fragment"}
port_data = pd.DataFrame(
    {
        "Age": port_data["t_age"].flatten() + 25 - 1,
        "pIncome": port_data["pLvl"].flatten(),
        "nrmM": port_data["mNrm"].flatten(),
        "nrmC": port_data["cNrm"].flatten(),
    }
)
port_data["Cons"] = port_data.nrmC * port_data.pIncome
port_data["M"] = port_data.nrmM * port_data.pIncome
```

```python editable=true slideshow={"slide_type": "slide"}
# Find the mean of each variable at every age
AgeMeans = port_data.groupby(["Age"]).median().reset_index()

# Create a figure and axis
fig, ax = plt.subplots()

sns.lineplot(x=AgeMeans.Age, y=AgeMeans.pIncome, label="Permanent Income", ax=ax)
sns.lineplot(x=AgeMeans.Age, y=AgeMeans.M, label="Market resources", ax=ax)
sns.lineplot(x=AgeMeans.Age, y=AgeMeans.Cons, label="Consumption", ax=ax)

# Set labels and title
ax.set_xlabel("Age")
ax.set_ylabel("Thousands of USD")
ax.set_title("Variable Medians Conditional on Survival")


# Show legend
ax.legend()

plt.show()
```
