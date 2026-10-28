/* Learning scaffolds derived from the canonical worksheets; no automatic grading. */
'use strict';
const LearningData = (() => {
  const field=(id,label,hint='',type='textarea',options=[])=>({id,label,hint,type,options});
  const group=(title,en,intro,fields)=>({title,en,intro,fields});
  const matrix=(prefix,rows,columns)=>rows.flatMap(([key,label])=>columns.map(([suffix,title,hint=''])=>({...field(`${prefix}_${key}_${suffix}`,title,hint),row:label})));
  const review=()=>group('回看、修订与披露','Review & revise','自评、同伴与教师反馈分别记录。提示用于检查证据，不替代你的判断。',[
    field('feedback_source','反馈来源','','select',['自我评审','同伴','教师']),
    field('feedback','具体反馈','检查对象是否明确、证据是否对应、结论是否超出材料。至少提出一条能执行的修改意见。'),
    field('response','我如何回应反馈','说明采纳、部分采纳或未采纳，以及理由。'),
    field('revision_before','修订前的关键表述','保留原文，以便与修订后比较。'),
    field('revision_after','修订后的关键表述','写下实际修改，不只写“已修改”。'),
    field('revision_reason','变化与新认识','这次修订解决了什么问题？还有什么未知？'),
    field('ai_used','是否使用 AI 协助','','select',['没有使用','使用了 AI']),
    field('ai_disclosure','AI 使用与责任说明','若使用：工具、环节、生成内容、核查方式与本人完成的判断；若未使用，请写“未使用”。')]);
  const activities=[
    {id:'ACT-CH01-01',evidence:'EVD-CH01-01',unit:'CH01',title:'从一次回答，到四种行动',en:'From an answer to four actions',minutes:'30–40',kind:'analysis',deliverable:'一份“使用—理解—创造”对照分析',summary:'把一个熟悉的 AI 体验，变成可以核查的问题与行动。',steps:[
      group('记录一个使用情境','Your starting point','选择自己最近使用的工具，或采用下面明确标为模拟的课堂情境。只记录必要摘要。',[
        field('tool','工具或产品名称','','text'),field('date','使用日期（大致即可）','','text'),field('task','我想完成什么任务'),field('input','必要输入摘要'),field('answer','回答或结果摘要'),field('intended_use','我准备怎样使用这个结果')]),
      group('提出三个理解问题','Three questions','把“可靠吗”拆成能够找到材料来核查的问题。',matrix('questions',[['1','问题 1'],['2','问题 2'],['3','问题 3']],[['question','我还不能确认的问题'],['why','为什么仅凭回答无法判断'],['evidence','需要什么材料或证据']])),
      group('比较四种行动','Four actions','使用、研究、修改与分享，需要的材料和条件可能不同。',matrix('actions',[['use','使用'],['study','研究'],['modify','修改'],['share','分享']],[['goal','我希望做什么'],['materials','所需材料与条件'],['limits','仍然存在的限制']])),
      group('比较三种学习位置','Learning positions','这三种位置不表示能力高低；一份核查指南也可以是一种创造。',matrix('positions',[['use','使用'],['understand','理解'],['create','创造']],[['gained','我已得到什么'],['unknown','还不能判断什么'],['next','下一步证据或行动']])),
      group('连接历史，保留边界','History & boundaries','回到本章的 GNU、Linux 或 OSI，而不是用软件故事证明 AI 的全部情况。',[
        field('history','历史坐标','','select',['GNU 与自由软件','Linux 与协作开发','OSI 与开源定义']),field('history_connection','它提醒我追问什么，为什么'),field('analogy_boundary','软件到 AI 的类比有什么边界'),field('boundary','目前可以说明、不能判断及还需补充的证据')]),review()]
    },
    {id:'ACT-CH01-02',evidence:'EVD-CH01-02',unit:'CH01',title:'画出我的学习问题地图',en:'Map your next question',minutes:'25–35',kind:'map',deliverable:'一页可继续修订的问题地图',summary:'把模糊好奇，转化为对象、证据、行动和贡献设想。',steps:[
      group('一个对象，一个黑盒','Choose your object','对象与版本可以未知；真实地保留未知比填入猜测更有用。',[
        field('object','对象名称','','text'),field('object_type','对象类型','','select',['工具','模型','数据集','应用','项目','其他']),field('version','版本或日期','不知道时填写“未知／待核查”。','text'),field('significance','为什么关注它'),field('black_box','我想打开的黑盒及其意义'),field('initial_question','最初的宽泛疑问'),field('core_question','改写后的可观察问题','说清对象、具体任务与可以找到的证据。')]),
      group('为问题寻找证据','Find evidence','不要求每一类都有。可写已有、待寻找、未知或不适用，并解释原因。',[
        ...matrix('evidence',[['code','代码'],['data','数据信息'],['parameters','参数或配置'],['docs','文档与版本'],['evaluation','评测材料'],['license','许可与使用条件'],['community','协作与维护']],[['reason','与问题的关系'],['status','目前状态：已有／待寻找／未知／不适用']]),field('priority','优先核查的 1—3 项及理由')]),
      group('迈出足够小的一步','A small next step','选择阅读、比较、核查、整理文档或设计评测等当前能完成的行动。',[
        field('next_action','准备做什么'),field('materials','需要什么材料'),field('duration','预计用时','','text'),field('output','会留下什么学习产物'),field('fallback','遇到困难的替代方案')]),
      group('设想贡献与后续路线','A possible contribution','这里是设想与计划，不表示已经参与真实社区。',[
        field('contribution_type','贡献形式','','select',['文档','数据','评测','翻译','设计','讨论','代码','其他']),field('contribution_need','回应什么真实需要'),field('beneficiaries','谁可能受益'),field('to_confirm','还需学习或确认什么'),field('unknowns','目前无法判断的事项'),field('unsupported','现有信息不能支持的结论'),field('next_chapters','准备在哪些后续章节回查','例如 CH07 许可与开放程度；请补充要回查的问题。'),field('change_record','问题改变时准备记录什么')]),review()]
    },
    {id:'ACT-CH02-01',evidence:'EVD-CH02-01',unit:'CH02',title:'打开，不等于已经可用',en:'From public to reusable',minutes:'35–45',kind:'releases',deliverable:'一份开放—复用—协作机制分析单',summary:'展开四次虚构发布，追踪材料、行动与证据之间的缺口。',simulated:true,steps:[
      group('先留下初始判断','Before you unfold','虚构项目“校园 AI 学习助手资料包”希望帮助新生检查 AI 回答。先只看“已公开发布”。',[
        field('initial_judgment','我最初认为别人可以做什么'),field('initial_evidence','哪些判断还需要证据')]),
      group('逐次展开四次发布','Four releases','使用下方发布观察器逐次比较。第四次也不等于公共价值已产生。',matrix('release',[['1','第一次 · 网页展示'],['2','第二次 · 完整下载与授权'],['3','第三次 · 复用材料'],['4','第四次 · 协作材料']],[['materials','新增材料或条件'],['actions','可能采取的行动'],['limits','仍不能推出的结论']])),
      group('追踪一次复用','Trace reuse','选择改编评测题、翻译指南、整合手册或自己的小目标。',[
        field('reuse_goal','具体复用目标'),...matrix('reuse',[['object','对象与文件'],['version','版本'],['rights','使用、修改和分享条件'],['docs','文档与示例'],['format','格式与必要依赖'],['source','来源与第三方内容'],['attribution','署名与修改说明'],['validation','改编后的验证']],[['evidence','已有证据'],['unknown','还需确认']]),field('reuse_explanation','为什么允许复用不等于顺利复用')]),
      group('拆开协作闭环','Trace collaboration','只对应案例给出的材料；没有记录的环节可明确写未知。',[
        ...matrix('collaboration',[['need','发现需要'],['context','了解情境'],['proposal','提出贡献'],['review','讨论与评审'],['decision','作出决定'],['release','发布变更'],['maintenance','持续维护']],[['evidence','案例中的证据'],['missing','缺少它可能发生什么']]),field('collaboration_explanation','为什么人数与讨论量不足以说明协作质量')]),
      group('找出三个断点','Find the gaps','条件、过程与实际结果，需要不同证据。',[
        field('gap_reuse','公开到复用：即使授权，仍可能因为什么难以复用'),field('gap_collaboration','复用到协作：改编很多，仍可能缺少什么'),field('gap_value','协作到公共价值：接纳贡献仍不能证明什么'),field('value_unknown_1','公共价值未知 1'),field('value_unknown_2','公共价值未知 2'),field('value_unknown_3','公共价值未知 3')]),review()]
    },
    {id:'ACT-CH02-02',evidence:'EVD-CH02-02',unit:'CH02',title:'练习一次可评审的贡献',en:'Design a reviewable contribution',minutes:'35–45',kind:'contribution',deliverable:'一份模拟贡献方案与公共价值说明',summary:'从一个小需要出发，保留初稿、模拟评审和实际修订。',simulated:true,steps:[
      group('从项目需要出发','Start with a need','虚构项目：校园 AI 学习助手资料包。阅读旁边的情境与规则，再选择一个小需要。',[
        field('need','我选择的项目需要'),field('affected','谁受到影响'),field('evidence','案例中的依据'),field('materials_reviewed','已查看的材料与版本'),field('to_confirm','还需向项目确认什么'),field('problem','如果不解决，谁会在什么任务中遇到什么困难')]),
      group('让范围足够小','Keep it small','一次贡献集中解决一个问题，便于理解、评审和维护。',[
        field('contribution_type','贡献形式','','select',['文档','数据','评测','翻译','设计','讨论','其他']),field('deliverable','准备交付什么'),field('scope','修改或新增哪个部分'),field('out_of_scope','本次明确不做什么'),field('materials','需要的材料'),field('validation','怎样检查交付物是否有效'),field('proposal','原始贡献说明','建议 150—250 字：情境、需要、交付物、来源与许可、自查和 AI 披露。')]),
      group('把维护者也考虑进来','Think about maintenance','让方案既可检查，也可持续。',[
        field('review_cost','理解与检查所需时间'),field('maintenance_cost','新增的后续维护工作'),field('licensing','第三方内容、来源与许可'),field('risks','隐私、偏见、错误传播或其他风险'),field('rejection_response','暂不接纳时怎样处理')]),
      group('进行模拟维护者评审','Simulated review','切换到维护者视角自评，或记录真实获得的同伴角色意见。系统不会替你编造反馈。',[
        field('review_source','评审来源','','select',['维护者视角自我评审','同伴角色评审','教师评审']),...matrix('review',[['need','需要是否具体且符合项目'],['scope','范围和交付物是否清楚'],['evidence','情境、来源和检查是否足够'],['cost','是否增加不必要的维护成本'],['risk','是否存在许可、隐私或误导风险']],[['comment','模拟评审意见']]),field('review_priority','最希望修改的一件事'),field('simulated_decision','模拟决定','','select',['接纳（模拟）','要求修改后复审（模拟）','暂不接纳（模拟）'])]),
      group('回应，然后真正修改','Respond & revise','保留初稿，写出回应和修订稿。不同意也需要说明理由。',[
        ...matrix('responses',[['1','反馈 1'],['2','反馈 2（若无请注明）']],[['feedback','反馈内容'],['response','我的回应'],['adoption','采纳／部分采纳／不采纳及理由']]),field('revised_proposal','修订后的贡献说明'),field('changes','具体修改了什么'),field('cost_reduction','如何降低理解、评审或维护成本'),field('remaining','仍保留的不同意见或未知')]),
      group('区分预期价值与证据','Value & evidence','模拟接纳不是实际受益。请保留未覆盖的人与成本。',[
        field('beneficiaries','预期受益者'),field('intended_outcome','希望改善的任务或结果'),field('observable_evidence','可观察的价值证据'),field('uncovered','未覆盖者或额外成本承担者'),field('unsupported','当前不能证明的结论'),field('ai_used','是否使用 AI','','select',['没有使用','使用了 AI']),field('ai_disclosure','AI 使用与最终责任','说明工具、用途、生成或修改的内容、核查方式，以及由谁完成模拟评审和最终修订；未使用请注明。')])]
    }
  ];
  const units={
    PREFACE:{short:'绪论',en:'Start with curiosity',headline:'一次提问背后，<br>藏着怎样的世界？',summary:'从熟悉的输入框出发，看见 AI 背后的材料、技术与共同劳动。',outcome:'留下你的第一个问题',explorer:'system',tag:'从好奇开始',order:'00'},
    CH01:{short:'第一章',en:'See beyond the answer',headline:'会使用 AI，<br>然后呢？',summary:'区分产品、模型与系统，沿着真实开放材料，练习有依据地理解。',outcome:'一份对照分析 + 一张问题地图',explorer:'materials',tag:'从答案到证据',order:'01'},
    CH02:{short:'第二章',en:'Learn to create together',headline:'开放之后，<br>共同创造如何发生？',summary:'沿着公开、复用与协作，理解一个成果如何被共同改进。',outcome:'一份机制分析 + 一份模拟贡献',explorer:'collaboration',tag:'从材料到共同工作',order:'02'},
    'APP-A':{short:'阅读指南',en:'Reading repositories',headline:'读懂仓库与固定版本',summary:'不用安装 Git，也能找到教材讨论的那一份材料。',outcome:'知道对象、材料与版本的区别',tag:'随时查阅',order:'A'}
  };
  const releases=[
    {title:'网页展示',tag:'01 / VISIBLE',body:'指南截图与部分评测题可以浏览。没有完整文件、版本号和权利说明。',en:'A page shows screenshots and sample questions. No complete files, version or rights statement.',hint:'看得见，仍未回答获得了哪些修改和分享的权利。'},
    {title:'下载与授权',tag:'02 / PERMISSION',body:'提供可编辑的完整文件，允许使用、修改和再分发，分享须保留作者与来源。仍无使用指南、来源和版本信息。',en:'Editable files and permission to use, modify and redistribute are provided, with attribution. Instructions, provenance and versions are still missing.',hint:'权利更明确，实际复用仍需要文档、来源和验证。'},
    {title:'复用材料',tag:'03 / REUSE',body:'在前次基础上增加 README、版本号、材料来源、格式说明、使用示例与复用清单。',en:'Adds a README, version, provenance, formats, examples and a reuse checklist.',hint:'具备更多复用条件，不保证所有情境都可用。'},
    {title:'协作材料',tag:'04 / COLLABORATION',body:'增加贡献指南、讨论区、变更评审、发布说明与维护者回应。接纳仍依据项目范围和质量要求。',en:'Adds contribution guidance, discussions, review records, release notes and maintainer responses.',hint:'可以观察协作过程，公共价值仍需实际受益、成本与风险证据。'}
  ];
  const system=[
    ['使用界面','Interface','一个问题与一段回答，是系统的可见出口。','输入、输出与产品说明','我得到的回答来自哪个产品与版本？'],
    ['应用与工具','Tools & applications','检索、工具、规则与人工检查可能共同参与任务。','检索记录、工具轨迹与流程说明','这条信息来自模型，还是外部材料？'],
    ['模型与推理','Models & inference','模型参数、版本和运行条件会影响输出。','模型卡、参数与配置','取得权重之后，还缺什么运行条件？'],
    ['数据与评测','Data & evaluation','材料选择与评测方式影响能力结论的适用范围。','数据说明、任务、样本与指标','这项结果测了什么，又没有测什么？'],
    ['协作与维护','People & maintenance','人们通过文档、数据、代码和讨论改进共同成果。','Issue、PR、版本与维护记录','一项改变怎样得到检查和回应？']
  ];
  const materials=[
    ['产品入口','Product access','聊天网站与 API 是访问服务的入口。','能定位使用入口。','不能由此推断产品所有组件开放。','README §5'],
    ['模型下载','Model downloads','固定 README 指向模型与蒸馏模型的下载页面。','能定位具体模型的参数获取入口。','不能证明训练过程或整套系统可复现。','README §3'],
    ['运行说明','Running locally','README 给出本地运行参考与推荐配置。','能找到运行所需的部分说明。','不能说明任意设备都能运行，也不是实测成功。','README §6'],
    ['评测与报告','Research & evaluation','技术报告与评测表提供任务、条件及报告结果。','能检查被报告的任务和结果。','不能推广到所有学科或真实应用。','README §4'],
    ['许可说明','Licensing','仓库及权重许可与部分蒸馏模型的上游条件分别说明。','需要按具体材料与版本核查条件。','不能把一份许可自动套到整个在线产品。','README §7'],
    ['仍待核查','Open questions','数据信息、训练代码与完整产品配置，需要逐项核对。','可以明确接下来的证据需求。','没在当前材料找到，不等于证明不存在。','CH01 §四']
  ];
  return {activities,units,releases,system,materials};
})();
if(typeof module!=='undefined')module.exports=LearningData;
