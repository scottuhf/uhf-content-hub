/* ══════════════════════════════════════════════════════════════════
   HOOK ARCHETYPE CLASSIFIER
   Shared concept-based classifier used by hook-library.html and
   content-database.html. Defines a library of NFL/fantasy-football
   hook archetypes with weighted multi-signal scoring.

   Each reel hook text is scored against every archetype's signal
   groups. A reel "belongs to" an archetype if score >= 3.

   Three-tier model:
     Tier 1: Archetype (concept)        e.g. "The Insider Reveal"
     Tier 2: Sub-section (flavor)       e.g. "Coach Says"
     Tier 3: Literal sub-pattern (opt)  e.g. "X said Y about Z"
══════════════════════════════════════════════════════════════════ */
(function (global) {

const HOOK_ARCHETYPES = [
  /* ───────────────────────────────────────────────────────── */
  {
    id: 'insider-reveal',
    name: 'The Insider Reveal',
    description: 'An authority figure said or revealed something newsworthy.',
    color: '#339AE9',
    icon: '🎤',
    signals: [
      { weight: 3, keywords: ['just said','said something','just revealed','just dropped','just admitted','just told','told reporters','told the media','confessed','dropped a bomb','came out and said','went on record','let slip','sounded off','spoke out','sources tell','sources say','source tells','source says','i\'m hearing','i hear that','word is','word on the street','behind the scenes','behind closed doors'] },
      { weight: 2, keywords: ['coach','head coach',' hc ','gm','general manager','analyst','scout','insider','source','sources','beat writer','reporter','expert','quote','quoted','interview','interviewed','tell me','told me'] },
      { weight: 1, keywords: ['should have every','should worry','listen up','need to hear','you need to know','pay attention'] },
    ],
    subSections: [
      { id: 'coach-says', name: 'Coach Says',
        signals: [
          { weight: 3, keywords: ['coach said','coach told','coach revealed','head coach said','hc said','coaching staff said','his coach','her coach','this coach'] },
          { weight: 2, keywords: ['mcvay','belichick','shanahan','reid','tomlin','daboll','campbell','vrabel','harbaugh','mcdaniel','sirianni','staley','quinn','payton'] },
        ],
      },
      { id: 'player-admits', name: 'Player Admits',
        signals: [
          { weight: 3, keywords: ['said he','told his','admitted he','admitted that','admitted to','revealed that he','was honest about','came clean','opened up about','was candid'] },
          { weight: 2, keywords: ['publicly','in an interview','postgame','presser','press conference'] },
        ],
      },
      { id: 'player-on-player', name: 'Player On Player',
        signals: [
          { weight: 3, keywords: ['said about','spoke about his teammate','about teammate','told us about','spoke about','calls out','called out','went after','took a shot at','threw shade','responded to'] },
        ],
      },
      { id: 'beat-reporter', name: 'Beat Reporter / Insider',
        signals: [
          { weight: 3, keywords: ['schefter','rapoport','glazer','per sources','per source','per report','reports that','first reported','breaking','breaking news','league sources','league source','tweet','tweeted','tweeting'] },
          { weight: 2, keywords: ['confirmed','reported','reporting','rumor mill'] },
        ],
      },
      { id: 'analyst-take', name: 'Analyst Take',
        signals: [
          { weight: 3, keywords: ['analyst','expert','believes','thinks','predicts','wrote about','says about','take on','his take','her take'] },
          { weight: 2, keywords: ['pat mcafee','tony romo','chris simms','kyle brandt','adam schefter','colin cowherd','stephen a','peter king'] },
        ],
      },
    ],
  },
  /* ───────────────────────────────────────────────────────── */
  {
    id: 'bold-prediction',
    name: 'The Bold Prediction',
    description: 'Strong forward-looking claim about what will happen.',
    color: '#9B59B6',
    icon: '🔮',
    signals: [
      { weight: 3, keywords: ['will be the next','going to be a','set to','will dominate','watch out','the next','breakout','breakout star','will become','my prediction','prediction is','calling it now','mark my words','book it','about to break out','about to explode','going to break out','primed for a breakout','breakout candidate','breakout season'] },
      { weight: 2, keywords: ['future','this season','this year','next season','you\'ll see','my pick to','my bet','my guess','primed','poised'] },
      { weight: 1, keywords: ['elite','generational','special','league mvp','dark horse','will finish'] },
    ],
    subSections: [
      { id: 'breakout-call', name: 'Breakout Call',
        signals: [
          { weight: 3, keywords: ['breakout','about to break out','about to explode','ready to break','primed for','poised for','breakout season','breakout candidate','breakout year','breakout player'] },
        ],
      },
      { id: 'bust-call', name: 'Bust Call',
        signals: [
          { weight: 3, keywords: ['bust','overrated','will disappoint','will fall','don\'t draft','avoid at all costs','overdrafted','reach','fade','letdown','overhyped'] },
        ],
      },
      { id: 'season-outlook', name: 'Season Outlook',
        signals: [
          { weight: 3, keywords: ['this season','this year','full season','will finish','top 5 at his position','rb1','wr1','qb1','te1','finish as','finish top'] },
          { weight: 2, keywords: ['projected','projection','outlook','season-long'] },
        ],
      },
      { id: 'long-term', name: 'Long-Term / Dynasty',
        signals: [
          { weight: 3, keywords: ['dynasty','keeper','years to come','long term','3 years','5 years','rookie contract','future star','franchise player','generational'] },
          { weight: 2, keywords: ['ceiling','floor','outlook','window'] },
        ],
      },
    ],
  },
  /* ───────────────────────────────────────────────────────── */
  {
    id: 'sleeper-pick',
    name: 'The Sleeper Pick',
    description: 'An under-the-radar opportunity nobody is talking about.',
    color: '#3ECF6A',
    icon: '💎',
    signals: [
      { weight: 3, keywords: ['sleeper','hidden gem','nobody is talking','no one is talking','nobody is drafting','sneaky pick','under the radar','overlooked','slept on','you should be drafting','dark horse','being slept on','flying under','undervalued','underdrafted','underrated'] },
      { weight: 2, keywords: ['hidden','quiet','ignored','late round','deep sleeper','value pick','steal','bargain','off the radar'] },
      { weight: 1, keywords: ['take a chance','gamble','flier','lottery ticket','dart throw'] },
    ],
    subSections: [
      { id: 'late-round', name: 'Late-Round Draft',
        signals: [
          { weight: 3, keywords: ['late round','round 10','round 11','round 12','round 13','round 14','15th round','last round','final round','final pick','round-by-round','late round flier','late round target'] },
          { weight: 2, keywords: ['draft target','draft sleeper','draft pick'] },
        ],
      },
      { id: 'waiver-fa', name: 'Free Agent / Waiver',
        signals: [
          { weight: 3, keywords: ['waiver','waiver wire','add him','add now','free agent pickup','should be added','pick him up','add this week','must add','priority add','top waiver','street free agent'] },
          { weight: 2, keywords: ['available','undrafted','undropped'] },
        ],
      },
      { id: 'position-change', name: 'Position-Change Sleeper',
        signals: [
          { weight: 3, keywords: ['new role','new position','new opportunity','expanded role','more touches','more targets','bigger role','promoted to','starter','rb1 role','wr1 role','feature back','workhorse role'] },
        ],
      },
      { id: 'coaching-change', name: 'Coaching-Change Sleeper',
        signals: [
          { weight: 3, keywords: ['new coach','new offensive coordinator','new oc','new head coach','coaching change','new staff','new system fits','perfect fit','fits the','should benefit','scheme fit','offensive scheme'] },
        ],
      },
    ],
  },
  /* ───────────────────────────────────────────────────────── */
  {
    id: 'cliff-warning',
    name: 'The Cliff Warning',
    description: 'An established asset is in trouble or losing value.',
    color: '#E74C3C',
    icon: '⚠️',
    signals: [
      { weight: 3, keywords: ['falling','plummeting','in trouble','in serious trouble','in big trouble','losing his job','lost his job','downhill','hitting a wall','cliff','off a cliff','hit the cliff','declining','on the decline','regression','regress','dropping fast','cooked','washed','washed up','in danger','about to fall','tanking','crashing','collapsing'] },
      { weight: 2, keywords: ['trouble','decline','falling off','struggle','struggling','worried','concerned','red flag','red flags'] },
      { weight: 1, keywords: ['risk','warning','careful','beware','watch out for'] },
    ],
    subSections: [
      { id: 'stock-falling', name: 'Stock Falling',
        signals: [
          { weight: 3, keywords: ['stock falling','stock dropping','stock down','value falling','value dropping','dynasty value falling','trade value falling','sell now','sell before','sell high','plummet','tumbling','crashing'] },
        ],
      },
      { id: 'usage-decline', name: 'Usage Decline',
        signals: [
          { weight: 3, keywords: ['snap count','snaps','touches','targets','target share','workload','rotational','timeshare','split backfield','splitting carries','benched','demoted','third string','backup','rotation','rotational role','snap percentage'] },
        ],
      },
      { id: 'injury-risk', name: 'Injury Risk',
        signals: [
          { weight: 3, keywords: ['injury','injuries','hurt','hamstring','knee','ankle','soft tissue','injury history','injury prone','health concern','pup list','ir','injured reserve','sidelined','out for the season','season ending'] },
        ],
      },
      { id: 'veteran-decline', name: 'Veteran Decline',
        signals: [
          { weight: 3, keywords: ['aging','past his prime','too old','done','age curve','30 year old','30+','final year','last legs','running out of time','end of career','retirement','retire','retirement consideration'] },
          { weight: 2, keywords: ['veteran','old vet','aging vet'] },
        ],
      },
      { id: 'scheme-mismatch', name: 'Scheme Mismatch',
        signals: [
          { weight: 3, keywords: ['doesn\'t fit','bad fit','wrong scheme','scheme mismatch','mismatch','clash','can\'t mesh','poor fit','wrong offense','wrong system','square peg','round hole'] },
        ],
      },
    ],
  },
  /* ───────────────────────────────────────────────────────── */
  {
    id: 'surprise-move',
    name: 'The Surprise Move',
    description: 'An unexpected trade, signing, cut, or draft pick.',
    color: '#FF6B35',
    icon: '🚨',
    signals: [
      { weight: 3, keywords: ['just got traded','just traded','traded to','shocking trade','surprise trade','blockbuster','blockbuster trade','just signed','signed with','breaking news','breaking','just cut','just released','released by','picked at','drafted to','going to','lands in','lands with','traded for','dealt to','deal sends','swap'] },
      { weight: 2, keywords: ['trade','signing','signed','traded','cut','released','draft pick','picked','drafted','contract'] },
      { weight: 1, keywords: ['destination','landing spot','new home','franchise change'] },
    ],
    subSections: [
      { id: 'trade', name: 'Trade',
        signals: [
          { weight: 3, keywords: ['traded to','trade to','trade lands','blockbuster trade','swap','shipped to','sent to','goes to','dealt to','deal sends','trade deadline','trade rumor','trade demand','requested a trade','demanding a trade'] },
        ],
      },
      { id: 'free-agency', name: 'Free Agency Signing',
        signals: [
          { weight: 3, keywords: ['free agent','signed with','contract','deal worth','million deal','year deal','agreed to terms','agreed with','reportedly signing','signing with','franchise tag','franchise tagged'] },
        ],
      },
      { id: 'cut-release', name: 'Cut / Release',
        signals: [
          { weight: 3, keywords: ['cut','released','waived','let go','released by','salary cap cut','cap casualty','cap cut','released ahead of','surprise cut','unceremoniously released'] },
        ],
      },
      { id: 'draft-selection', name: 'Draft Selection',
        signals: [
          { weight: 3, keywords: ['drafted','first round','second round','third round','round 1','round 2','round 3','number one pick','#1 pick','top pick','overall pick','goes to the','at pick','draft class','rookie','draft night','draft day'] },
        ],
      },
    ],
  },
  /* ───────────────────────────────────────────────────────── */
  {
    id: 'stat-bomb',
    name: 'The Stat Bomb',
    description: 'A counterintuitive or eye-catching statistic.',
    color: '#3ECF6A',
    icon: '📊',
    signals: [
      { weight: 3, keywords: ['did you know','more than','leads the league','leads in','ranks first','ranks #1','percent of','% of','averaged','only player to','only one to','history of','all time','in history','broke the record','broke a record','set a new','never been done','first time ever','tied for','among the league','among the top'] },
      { weight: 2, keywords: ['stat','stats','statistic','statistically','numbers','by the numbers','data','fact','facts','percentile','league wide'] },
      { weight: 1, keywords: ['impressive','ridiculous','insane stat','crazy stat'] },
    ],
    subSections: [
      { id: 'historic', name: 'Historic Stat',
        signals: [
          { weight: 3, keywords: ['all time','in history','first since','first ever','first to do','only player to','broke the record','set a record','never been done','since 19','since 20','all-time list','franchise record','league record'] },
        ],
      },
      { id: 'comparison-stat', name: 'Comparison Stat',
        signals: [
          { weight: 3, keywords: ['more than','fewer than','less than','same as','equal to','ahead of','behind','outpaces','outperforms','compared to','than any other','double the','triple the','half the'] },
        ],
      },
      { id: 'hidden-trend', name: 'Hidden Trend',
        signals: [
          { weight: 3, keywords: ['did you know','few people know','no one talks about','surprising stat','underrated stat','quietly leads','quietly the','quietly has','sneaky stat','overlooked stat'] },
        ],
      },
      { id: 'volume', name: 'Volume Stat',
        signals: [
          { weight: 3, keywords: ['target share','snap share','touches per game','attempts per','red zone','red-zone','goal line','high volume','volume play','workload','usage rate','snap percentage','target percentage'] },
        ],
      },
    ],
  },
  /* ───────────────────────────────────────────────────────── */
  {
    id: 'ranking-tier',
    name: 'The Ranking / Tier List',
    description: 'List-format content ranking players, picks, or moves.',
    color: '#FFD700',
    icon: '🏆',
    signals: [
      { weight: 3, keywords: ['top 3','top 5','top 7','top 10','top 15','top 20','top 25','my ranking','my top','these 3','these 5','these 7','these 10','3 players','5 players','7 players','3 reasons','5 reasons','7 reasons','3 ways','5 ways','list of','best of','worst of','my favorite','my pick for'] },
      { weight: 2, keywords: ['tier','tiers','ranked','ranks','list','rankings'] },
      { weight: 1, keywords: ['best','worst','top','bottom','greatest','elite tier'] },
    ],
    subSections: [
      { id: 'top-n', name: 'Top N',
        signals: [
          { weight: 3, keywords: ['top 3','top 5','top 7','top 10','best of','best in the','my favorite','best 3','best 5','best players','best fits','my top'] },
          { weight: 2, keywords: ['most','greatest','elite'] },
        ],
      },
      { id: 'worst-n', name: 'Worst N',
        signals: [
          { weight: 3, keywords: ['worst','bottom 3','bottom 5','avoid these','don\'t draft','overrated 3','overrated 5','biggest busts','3 busts','5 busts','worst picks','red flag players'] },
        ],
      },
      { id: 'tier-drop', name: 'Tier Drop',
        signals: [
          { weight: 3, keywords: ['tier','tiers','tier 1','tier 2','tier 3','tier drop','tier list','dropping a tier','top tier','elite tier','tier upgrade'] },
        ],
      },
      { id: 'my-favorites', name: 'My Favorites',
        signals: [
          { weight: 3, keywords: ['my favorite','my favorites','my picks','my top','my personal','my guys','my targets','my list','my draft targets'] },
        ],
      },
    ],
  },
  /* ───────────────────────────────────────────────────────── */
  {
    id: 'comparison-vs',
    name: 'The Comparison / Versus',
    description: 'Direct head-to-head framing between players or choices.',
    color: '#ED0A73',
    icon: '⚔️',
    signals: [
      { weight: 3, keywords: [' vs ',' versus ','would you take','would you rather','rather have','who would you','who you taking','which is better','which one would','head to head','head-to-head','against','choose between','who wins','who\'s better','who would you take','who you rather','take first','draft first'] },
      { weight: 2, keywords: ['comparison','compared to','comparable','similar to'] },
      { weight: 1, keywords: ['pick one','your pick','this or that'] },
    ],
    regex: [/\b\w+\s+vs\.?\s+\w+/i, /\b\w+\s+or\s+\w+\s*\?/i],
    subSections: [
      { id: 'player-vs-player', name: 'Player vs Player',
        signals: [
          { weight: 3, keywords: [' vs ',' versus ',' or ','head to head','head-to-head','one on one','better than','similar to'] },
        ],
      },
      { id: 'trade-value', name: 'Trade Value',
        signals: [
          { weight: 3, keywords: ['trade for','trade value','would you trade','trade away','give up','sell to acquire','target in trade','trade target','fair trade','trade offer'] },
        ],
      },
      { id: 'draft-decision', name: 'Draft Decision',
        signals: [
          { weight: 3, keywords: ['take first','draft first','first off the board','draft order','round one decision','rd 1 decision','at pick','#1 overall','first overall','first pick'] },
        ],
      },
      { id: 'position-battle', name: 'Position Battle',
        signals: [
          { weight: 3, keywords: ['battle','starting','starting job','depth chart','rb1 of','wr1 of','starter','backup','will start','starting role','win the job','win the battle','snap split','timeshare battle','training camp battle'] },
        ],
      },
    ],
  },
  /* ───────────────────────────────────────────────────────── */
  {
    id: 'buy-sell-hold',
    name: 'The Buy / Sell / Hold',
    description: 'Judgment frame asking the viewer to decide value.',
    color: '#FF6B35',
    icon: '💰',
    signals: [
      { weight: 3, keywords: ['buy now','buy low','sell high','sell now','dynasty buy','dynasty sell','sell before','buy before','time to sell','time to buy','target in trade','sell window','buy window','buy sell hold','buy/sell','sell/buy','buy sell or hold','buy, sell or hold','buy, sell, or hold','make a move on','time to make a move'] },
      { weight: 2, keywords: [' buy ',' sell ',' hold ','value','stock','dynasty value','dynasty stock'] },
      { weight: 1, keywords: ['dynasty','keeper'] },
    ],
    subSections: [
      { id: 'buy-now', name: 'Buy Now',
        signals: [
          { weight: 3, keywords: ['buy now','buy low','buy before','target in trade','acquire','add him now','this is your chance','last chance to buy','steal','value buy','buying opportunity'] },
        ],
      },
      { id: 'sell-high', name: 'Sell High',
        signals: [
          { weight: 3, keywords: ['sell high','sell now','sell before','time to sell','offload','move on','flip him','flip for','window is closing','cash in','sell window'] },
        ],
      },
      { id: 'hold', name: 'Hold',
        signals: [
          { weight: 3, keywords: ['hold','don\'t sell','don\'t move','keep him','stay patient','let him cook','give it time','wait it out','patience','hold tight'] },
        ],
      },
      { id: 'dynasty-move', name: 'Dynasty Move',
        signals: [
          { weight: 3, keywords: ['dynasty buy','dynasty sell','dynasty hold','keeper league','dynasty move','dynasty value','dynasty stock','dynasty trade'] },
        ],
      },
    ],
  },
  /* ───────────────────────────────────────────────────────── */
  {
    id: 'backstory',
    name: 'The Backstory',
    description: 'Origin story or personal history reveal.',
    color: '#9B59B6',
    icon: '📖',
    signals: [
      { weight: 3, keywords: ['before he was','before he got drafted','before he made it','who is','story behind','his backstory','his story','his journey','came from','started as','used to be','his background','his roots','where it all started','his beginnings','grew up'] },
      { weight: 2, keywords: ['story','journey','history','past','beginnings'] },
      { weight: 1, keywords: ['origins','roots'] },
    ],
    subSections: [
      { id: 'origin-story', name: 'Origin Story',
        signals: [
          { weight: 3, keywords: ['before he was','where he came from','his roots','his beginnings','started as','before he got drafted','before he made it','came from','from humble','was a kid','high school days','college days','undrafted'] },
        ],
      },
      { id: 'personal-history', name: 'Personal History',
        signals: [
          { weight: 3, keywords: ['off the field','his family','his mom','his dad','his wife','his kid','his story','his personal','his life','grew up','childhood','high school','college'] },
        ],
      },
      { id: 'past-success', name: 'Past Success Reminder',
        signals: [
          { weight: 3, keywords: ['remember when','remember the','his rookie year','his breakout','he did this','already proved','don\'t forget','remember he','years ago','flashback','throwback'] },
        ],
      },
    ],
  },
  /* ───────────────────────────────────────────────────────── */
  {
    id: 'trend-pattern',
    name: 'The Trend Pattern',
    description: 'Multi-data-point observation about a recurring pattern.',
    color: '#339AE9',
    icon: '📈',
    signals: [
      { weight: 3, keywords: ['every time','always happens','history shows','since 20','since 19','in the past','traditionally','every year','every season','the pattern','consistent pattern','repeats','repeats itself','last 5 years','last 10 years','last 3 years','last 7 years','this has happened','same story','déjà vu','deja vu'] },
      { weight: 2, keywords: ['pattern','trend','history','historically','consistently'] },
      { weight: 1, keywords: ['rinse and repeat','same as last','here we go again'] },
    ],
    subSections: [
      { id: 'historical-pattern', name: 'Historical Pattern',
        signals: [
          { weight: 3, keywords: ['since 19','since 20','in the past','last 5 years','last 10 years','last 3 years','history says','history shows','every time','traditionally','since the','since this','for years'] },
        ],
      },
      { id: 'position-trend', name: 'Position Trend',
        signals: [
          { weight: 3, keywords: ['rookie wrs','rookie rbs','rookie qbs','rookie tes','second year','third year','sophomore','year 2','year 3','at this age','at his position','position trend','positional value'] },
        ],
      },
      { id: 'coaching-pattern', name: 'Coaching Pattern',
        signals: [
          { weight: 3, keywords: ['his coaches','his offense','his system','this scheme','this offensive coordinator','this oc','his coordinator','coach\'s record','his coach always','offenses he coaches','offenses he runs','this play caller'] },
        ],
      },
    ],
  },
  /* ───────────────────────────────────────────────────────── */
  {
    id: 'hot-take',
    name: 'The Hot Take / Contrarian',
    description: 'A claim that pushes against the consensus view.',
    color: '#E74C3C',
    icon: '🔥',
    signals: [
      { weight: 3, keywords: ['nobody wants to admit','no one wants to admit','hot take','unpopular opinion','controversial','controversial take','the truth','real talk','honest take','brutal truth','harsh truth','unpopular','against the grain','contrarian','wake up','consensus is wrong','they\'re all wrong','everyone is wrong'] },
      { weight: 2, keywords: ['opinion','take','truth','honest','brutal','harsh','spicy take'] },
      { weight: 1, keywords: ['facts','real','honest opinion'] },
    ],
    subSections: [
      { id: 'unpopular-opinion', name: 'Unpopular Opinion',
        signals: [
          { weight: 3, keywords: ['unpopular opinion','hot take','controversial','controversial take','my take','my hot take','spicy take','cold take','frozen take'] },
        ],
      },
      { id: 'industry-wrong', name: 'Industry-Wrong Take',
        signals: [
          { weight: 3, keywords: ['everyone is wrong','everyone\'s wrong','consensus is wrong','industry is wrong','they\'re all wrong','wrong about','rankings are wrong','adp is wrong','groupthink','consensus pick'] },
        ],
      },
      { id: 'nobody-admits', name: 'Nobody Admits',
        signals: [
          { weight: 3, keywords: ['nobody wants to admit','no one wants to admit','nobody talks about','no one talks about','the dirty secret','dirty little secret','elephant in the room','can\'t deny','must admit','hidden truth','no one will say'] },
        ],
      },
    ],
  },
  /* ───────────────────────────────────────────────────────── */
  {
    id: 'meme-reaction',
    name: 'The Meme / Reaction',
    description: 'Humor-driven, low-info, high-engagement format.',
    color: '#FFD700',
    icon: '😂',
    signals: [
      { weight: 3, keywords: ['meme','lol','lmao',' pov ','pov:',' mood ','vibes','energy','react','reaction','my reaction','when X happens','the way','the moment','sound on','trending audio'] },
      { weight: 2, keywords: ['joke','funny','comedic','hilarious','laugh','laughing','dead','gone'] },
      { weight: 1, keywords: ['me when','this is me'] },
    ],
    subSections: [
      { id: 'react', name: 'React Format',
        signals: [
          { weight: 3, keywords: ['my reaction','reaction to','reacting to','reacts to','watch me react','react video','first time hearing','first time seeing','live reaction','reaction video'] },
        ],
      },
      { id: 'meme-template', name: 'Meme Template',
        signals: [
          { weight: 3, keywords: ['pov','mood','vibes','the way','the moment','when X','me when','this is me','trending audio','sound on','tiktok trend','reels trend','using the','this audio'] },
        ],
      },
      { id: 'joke-punchline', name: 'Joke / Punchline',
        signals: [
          { weight: 3, keywords: ['lol','lmao','joke','funny','hilarious','i\'m dead','i\'m gone','rotfl','i\'m crying','can\'t stop laughing','dying','comedy gold','can\'t breathe'] },
        ],
      },
    ],
  },
  /* ───────────────────────────────────────────────────────── */
  {
    id: 'suspense-tease',
    name: 'The Suspense Tease',
    description: 'Building anticipation for an upcoming payoff.',
    color: '#FF6B35',
    icon: '🎬',
    signals: [
      { weight: 3, keywords: ['wait until you see','you won\'t believe','you have to see this','watch this','watch what happens','hold on','listen to this','get ready','stop scrolling','before you scroll','just wait','i have to show you','you need to see','can\'t believe','can not believe','unbelievable','wait for it','wait til','wait till'] },
      { weight: 2, keywords: ['crazy','insane','ridiculous','wild','unreal'] },
      { weight: 1, keywords: ['wait','watch','listen'] },
    ],
    subSections: [
      { id: 'wait-until', name: '"Wait Until You See"',
        signals: [
          { weight: 3, keywords: ['wait until you see','wait for it','wait until you hear','just wait','wait til','wait till','keep watching','watch this','watch what happens'] },
        ],
      },
      { id: 'wont-believe', name: '"You Won\'t Believe"',
        signals: [
          { weight: 3, keywords: ['you won\'t believe','won\'t believe','can\'t believe','i don\'t believe','no way','no chance','unbelievable','unreal','crazy thing','this is wild'] },
        ],
      },
      { id: 'have-to-show', name: '"Have To Show You"',
        signals: [
          { weight: 3, keywords: ['i have to show you','need to show you','have to see this','need to see','let me show you','let me tell you','listen up','pay attention','watch closely'] },
        ],
      },
    ],
  },
  /* ───────────────────────────────────────────────────────── */
  {
    id: 'direct-question',
    name: 'The Direct Question',
    description: 'Opens with a direct question to the viewer.',
    color: '#339AE9',
    icon: '❓',
    signals: [
      { weight: 3, keywords: ['did you know','do you know','can you name','can you guess','what if','what happens if','quiz time','this trivia','ask yourself','riddle me this','question for you','here\'s a question'] },
      { weight: 2, keywords: ['why is','why does','why are','how does','how can','what do you think','agree or disagree','tell me','comment below'] },
      { weight: 1, keywords: ['question','ask yourself'] },
    ],
    /* Direct Question is a fallback — only fires when the hook is PRIMARILY a question,
       not when another archetype just happens to phrase itself as one. We intentionally
       do NOT count "?" alone, since most short-form hooks end with a question mark. */
    subSections: [
      { id: 'trivia', name: 'Trivia',
        signals: [
          { weight: 3, keywords: ['did you know','do you know','can you name','can you guess','test your','quiz time','trivia','this trivia','guess who','name the','find the'] },
        ],
      },
      { id: 'opinion-solicit', name: 'Opinion Solicit',
        signals: [
          { weight: 3, keywords: ['who do you','what do you','how do you feel','what\'s your take','your thoughts','let me know','tell me','comment below','agree','disagree','vote','poll'] },
        ],
      },
      { id: 'hypothetical', name: 'Hypothetical',
        signals: [
          { weight: 3, keywords: ['what if','imagine if','what would happen','what would you','if you could','if X then','suppose','hypothetically','in a world where','what would'] },
        ],
      },
    ],
  },
  /* ───────────────────────────────────────────────────────── */
  {
    id: 'player-spotlight',
    name: 'The Player Spotlight',
    description: 'Focused single-player analysis or breakdown.',
    color: '#5a8ab0',
    icon: '🔍',
    signals: [
      { weight: 3, keywords: ['looking at','breaking down','deep dive','deep dive into','profile of','profile on','analysis of','analysis on','situation for','role for','fit for','outlook for','outlook on','breakdown of','his game','his tape','film breakdown'] },
      { weight: 2, keywords: ['breakdown','profile','analysis','situation','role','fit','outlook'] },
      { weight: 1, keywords: ['focused on','all about','spotlight'] },
    ],
    subSections: [
      { id: 'situation-analysis', name: 'Situation Analysis',
        signals: [
          { weight: 3, keywords: ['his situation','his role','his fit','his offense','depth chart','his coach','his snap count','his usage','his offensive line','his target share','his backfield'] },
        ],
      },
      { id: 'performance-review', name: 'Performance Review',
        signals: [
          { weight: 3, keywords: ['his stats','his numbers','his performance','his game','his season','his year','his week','his recent','his last','his past','his film'] },
        ],
      },
      { id: 'outlook-projection', name: 'Outlook / Projection',
        signals: [
          { weight: 3, keywords: ['his outlook','his projection','his ceiling','his floor','what to expect','expectations','range of outcomes','best case','worst case','realistic outcome','his upside','his downside'] },
        ],
      },
    ],
  },
];

/* ══════════════════════════════════════════════════════════════════
   SCORING ENGINE
══════════════════════════════════════════════════════════════════ */

function normalizeText(s) {
  // Add space around to make boundary checks easier; preserve % and ?
  return ' ' + String(s || '').toLowerCase() + ' ';
}

function scoreAgainst(text, definition) {
  if (!text || !definition) return 0;
  const t = normalizeText(text);
  let score = 0;
  if (definition.signals) {
    for (const group of definition.signals) {
      let hit = false;
      for (const kw of group.keywords) {
        if (t.includes(kw.toLowerCase())) { hit = true; break; }
      }
      if (hit) score += group.weight;
    }
  }
  if (definition.regex && Array.isArray(definition.regex)) {
    for (const re of definition.regex) {
      try { if (re.test(text)) score += 3; } catch (e) {}
    }
  }
  if (definition.excludeIf && definition.excludeIf.keywords) {
    for (const kw of definition.excludeIf.keywords) {
      if (t.includes(kw.toLowerCase())) return 0;
    }
  }
  return score;
}

/* Classify a single reel's hook text.
   Returns: { archetypes: [{ id, score, subSectionId, subSectionScore, allArchetypeScores }], primary, secondaries, density }
   or null if nothing scored above threshold. */
function classifyReel(text, archetypes) {
  archetypes = archetypes || HOOK_ARCHETYPES;
  if (!text) return null;
  const scored = [];
  for (const a of archetypes) {
    const score = scoreAgainst(text, a);
    if (score >= 3) {
      // Best sub-section within this archetype
      let bestSub = null, bestSubScore = 0;
      if (a.subSections) {
        for (const sub of a.subSections) {
          const sScore = scoreAgainst(text, sub);
          if (sScore > bestSubScore) { bestSubScore = sScore; bestSub = sub; }
        }
      }
      scored.push({
        archetypeId: a.id,
        score,
        subSectionId: bestSubScore >= 2 ? bestSub.id : 'general',
        subSectionScore: bestSubScore >= 2 ? bestSubScore : 0,
      });
    }
  }
  if (!scored.length) {
    // Compute near-miss for tray hint
    let bestNear = null;
    for (const a of archetypes) {
      const s = scoreAgainst(text, a);
      if (!bestNear || s > bestNear.score) bestNear = { archetypeId: a.id, score: s };
    }
    return { archetypes: [], primary: null, secondaries: [], density: 0, nearMiss: bestNear };
  }
  scored.sort((a, b) => b.score - a.score);
  const primary = scored[0];
  const secondaries = scored.slice(1).filter(s => s.score >= 2 && s.score >= primary.score * 0.5);
  return {
    archetypes: scored,
    primary: primary.archetypeId,
    primarySubSection: primary.subSectionId,
    secondaries: secondaries.map(s => s.archetypeId),
    density: scored.length,
  };
}

/* Classify every reel. Returns Map<reelId, classification>. */
function classifyAll(reels, archetypes) {
  const out = new Map();
  for (const r of reels) {
    if (!r.text) continue;
    const c = classifyReel(r.text, archetypes);
    if (c) out.set(r.id, c);
  }
  return out;
}

/* Convenience: find the single best archetype for a hook (used by
   the suggest-archetype toast on content-database.html). Returns
   { archetype, score } or null. */
function findBestArchetype(text, archetypes) {
  archetypes = archetypes || HOOK_ARCHETYPES;
  if (!text) return null;
  let best = null;
  for (const a of archetypes) {
    const s = scoreAgainst(text, a);
    if (s >= 3 && (!best || s > best.score)) best = { archetype: a, score: s };
  }
  return best;
}

/* ══════════════════════════════════════════════════════════════════
   TIER 3 — LITERAL SUB-PATTERN CLUSTERING (within a sub-section)
══════════════════════════════════════════════════════════════════ */
function _normalize(s) { return String(s||'').toLowerCase().replace(/[^a-z0-9\s]/g,' ').replace(/\s+/g,' ').trim(); }
function _trigrams(s) {
  const t = _normalize(s);
  const out = new Set();
  if (t.length < 3) return out;
  for (let i = 0; i <= t.length - 3; i++) out.add(t.slice(i, i+3));
  return out;
}
function _jaccard(a, b) {
  if (!a.size || !b.size) return 0;
  let inter = 0;
  a.forEach(x => { if (b.has(x)) inter++; });
  return inter / (a.size + b.size - inter);
}

function clusterLiteralPatterns(reels, threshold) {
  threshold = threshold || 0.42;
  const eligible = reels.filter(h => h.text && h.text.trim().split(/\s+/).length >= 3);
  if (!eligible.length) return [];
  const sets = eligible.map(h => ({ h, t: _trigrams(h.text) }));
  const visited = new Array(sets.length).fill(false);
  const clusters = [];
  for (let i = 0; i < sets.length; i++) {
    if (visited[i]) continue;
    const cluster = [sets[i].h];
    visited[i] = true;
    for (let j = i + 1; j < sets.length; j++) {
      if (visited[j]) continue;
      if (_jaccard(sets[i].t, sets[j].t) >= threshold) {
        cluster.push(sets[j].h);
        visited[j] = true;
      }
    }
    if (cluster.length >= 2) clusters.push(cluster);
  }
  return clusters;
}

function deriveLiteralTemplate(cluster) {
  const wordLists = cluster.map(h => _normalize(h.text).split(' '));
  if (!wordLists.length) return '';
  const minWords = Math.min(...wordLists.map(w => w.length));
  const threshold = Math.max(2, Math.ceil(cluster.length * 0.6));
  const result = [];
  let lastWasSlot = false;
  for (let i = 0; i < minWords; i++) {
    const counts = {};
    wordLists.forEach(w => { counts[w[i]] = (counts[w[i]] || 0) + 1; });
    const [topWord, topCount] = Object.entries(counts).sort((a, b) => b[1] - a[1])[0];
    if (topCount >= threshold && topWord.length > 2) {
      result.push(topWord);
      lastWasSlot = false;
    } else if (!lastWasSlot) {
      result.push('___');
      lastWasSlot = true;
    }
  }
  if (result.length && result[0] !== '___') {
    result[0] = result[0].charAt(0).toUpperCase() + result[0].slice(1);
  }
  return result.join(' ').replace(/(\s*___\s*)+/g, ' ___ ').trim();
}

/* ══════════════════════════════════════════════════════════════════
   EXPORT
══════════════════════════════════════════════════════════════════ */
global.HookArchetypes = {
  ARCHETYPES: HOOK_ARCHETYPES,
  scoreAgainst,
  classifyReel,
  classifyAll,
  findBestArchetype,
  clusterLiteralPatterns,
  deriveLiteralTemplate,
};

})(typeof window !== 'undefined' ? window : globalThis);
