import csv
import io
# CSV data as a string
# open csv file #
csv_data = """ƒ,,,,,,
Rachel Skubel,@rachelskubel,rskubel@gmail.com,Grad Student,www.rachelskubel.com,Adobe Spark,Marine/Conservation Science
May Carlon,@KristineJonson,carlon.m.aa@m.titech.ac.jp,Grad Student,maycarlon.com,Blogger,Educational Technology
Tia Martineau,@tia_martineau,tia.martineau@gmail.com,Grad Student,www.tiamartineau.science,Blogger,(supposedly) Gravitational wave detection/space instrumentation (but we'll see)
Zeke Piskulich,@zekepiskulich,ezekielpiskulich@gmail.com,Grad Stduent,https://piskulich.com,Bluehost + Wordpress,Computational Chemistry
Ubadah Sabbagh,@Neubadah,ubadahs@vt.edu,Grad Student,ubadahsabbagh.com,Custom,Neuroscience
Jonny Saunders,@json_dirs,jlsaunders987@gmail.com,Grad Student,https://jon-e.net,custom (https://github.com/sneakers-the-rat/sneakers-the-rat.github.io),Neuroscience
Amit Seal Ami,@lordamit,actually@not.a.good.idea,Grad Student,https://amitsealami.github.io,Github,Computer Science
Biplabendu Das,@another_ant_guy,biplabendu.das@gmail.com,Grad Student,https://biplabendu.github.io/homepage/,Github,"Social Insect Behavior, Parasitic Manipulation of Behavior, Myrmecology"
Emily Jones,@emilyasterjones,emily.jones@ucsf.edu,Grad Student,https://emilyasterjones.github.io/,Github,Neuroscience
Erik Reinertsen,@erikrtn,er@gatech.edu,Grad Student,erikreinertsen.com,GitHub,Biomedical informatics & machine learning
Katie Mummah ,@nuclearkatie ,mummah@wisc.edu,Grad Student,nuclearkatie.com,Github,"Nuclear engineering, nuclear nonproliferation, energy"
Kevin Yang,@YangKevinK,yangkky@gmail.com,Grad student,yangkky.github.io,Github,Computational biology and machine learning
Luis M. Montilla,@luismmontilla,luismmontilla@gmail.com,Grad Student,http://luismmontilla.github.io/,Github,Coral reef ecology
Marc Chevrette,@wildtypeMC,chevrette@wisc.edu,,chevrm.github.io,Github,"Microbial genomics, evolution of secondary metabolism"
Rosalie Bruel,@RosalieBruel,rosaliebruel@gamail.com,Post Doc ,https://rosalieb.github.io/rosaliebruelweb/index.html,GitHub,"Freshwater ecology, paleolimnology, food web models"
Adam Orr,@adamjorr,ajorr1@asu.edu,Grad Student,www.adamjorr.com,GitHub + Namecheap,Bioinformatics
Jon Albo,@jon_albo,Jea264@cornell.edu,Grad Student,https://jonalbo.com,Github + Namecheap,Biomedical Engineering
May Helena Plumb ,@mayhplumb,mayhplumb@utexas.edu ,Grad Student ,www.mayhplumb.com,Github + Namecheap,Linguistics (language documentation and description) 
Tom Burns,@tfburns,t.f.burns@gmail.com,Grad Student,https://tfburns.com,GitHub Pages,Artificial Intelligence / Computational Neuroscience
Julie Blommaert,@julie_b92,jblommaert92@gmail.com,Grad Student,julie.blommaert.com,Github+GoDaddy,Evolutionary genomics
Joseph Stachelek,@__jsta,stachel2@msu.edu,Grad Student,https://jsta.rbind.io,https://support.rbind.io/about/,"Ecosystem ecology, Freshwater ecology, Marine Science"
Juan C. Sanchez-Arias,@JuCamilo,juansa@uvic.ca,Grad Student,juansanar.com,Hugo Academic,"Neurobiology, developmental neurobiology"
Tyler Prochnow,@tyler_prochnow,tyler_prochnow1@baylor.edu,Grad Student,tprochnow.com,"Hugo-Academic, Netlify, Markdown",Network analysis and Health
Guillaume Dury,@gjdury,guillaume.dury@mail.mcgill.ca,Grad Student,www.gjdury.com,Namecheap + hosting server,"Entomology, Evolution"
Brandt Gaches,,bgaches@astro.umass.edu,Grad Student,http://brandt-gaches.space,NearlyFreeSpeech,Astronomy - star formation & astrochemistry
Carl Pearson,@carljpearson,cjp.uxr@gmail.com,Industry (post PhD),https://carljpearson.com/,Netlify + gitlab (domain via namecheap.com),"Psychology, human factors (usability, trust in automation)"
Dani Crain,@DCrainium,dani_crain@baylor.edu,Grad Student,https://danicrain.netlify.com/,"Netlify, R blogdown, Hugo Academic theme",Marine mammal physiology
Kevin Hardegree-Ullman,@kevinkhu,kevinkhu@caltech.edu,Post Doc,http://kevinkhu.com,Personal Server/Raspberry Pi,"Astrophysics (exoplanets, low mass stars, brown dwarfs)"
Erika Romero,@EverEducating,Erikar@evereducating.com,Grad Student,Www.evereducating.com,Siteground and Wordpress,"English, children’s and young adult literature (my blog is about higher ed teaching tips)"
Brea McCauley,@brea_mccauley,bmccaule@sfu.ca,Grad Student,breamccauley.com,Square Space,Archaeology (Evolution of religious rituals)
Anna Bax,@annastrikesbax,bax@ucsb.edu,Grad Student,annabax.org,Squarespace,Sociocultural linguistics
Ashlee Dauphinais,@ashenpashen,dauphinais.1@osu.edu,Grad student,www.ashleynedes.com,SquareSpace,Linguistics (Spanish & Portuguese sociocultural linguistics/linguistic anthropology)
Chase LaDue,@chaseladue,cladue@gmu.edu,Grad Student,www.cladue.org,Squarespace,"Animal behavior, conservation biology"
Danielle Mai,@daniellejmai,djmai@mit.edu,Post Doc,http://www.daniellejmai.com,Squarespace,"Polymer physics, biopolymers, chemical engineering"
Jordan Harrod,@jordanbharrod,jordan.b.harrod@gmail.com,Grad Student,www.jordanharrod.com,Squarespace,"AI for medicine, science communication "
Meredith Schmehl,@MeredithSchmehl,hello@meredithschmehl.com,Grad Student,meredithschmehl.com,Squarespace,"Neuroscience/neurobiology (sensory processing), science communication, science policy"
Rachel Kratofil,@rachelkratofil,rachel.kratofil@ucalgary.ca,Grad Student,www.immunews.com,Squarespace,Immunology
Ward Howard,@WardHoward4Him,wshoward@unc.edu,Grad student,http://wardhoward.web.unc.edu/,UNC Wordpress,"Astrophysics (exoplanets, space weather, instrumentation)"
Taylor Smith,@taylorsmith2,tsmith@cs.queensu.ca,Grad Student,http://cs.queensu.ca/~tsmith/,University,Theoretical computer science/mathematics
Name,Twitter Handle,Email,Grad Student/post doc,Website Link,Website Host,Research Area
Alexandra Brumberg,@nanobrumberg,brumberg@u.northwestern.edu,Grad Student,https://brumberg.weebly.com/,Weebly,Chemistry (nanomaterials)
Anat Etzion-Fuchs,@AnatEtzionFuchs,anatf@princeton.edu,Grad Student,anatetzionfuchs.com,Weebly,"Computational biology, machine learning"
Brandon Semel,@brandonsemel,bsemel@vt.edu,Grad student,https://brandonsemel.weebly.com/,Weebly,"Primatology, Conservation, Global Change"
Brett Morgan,@vagr_ant,bmorgan@hku.hk,Grad Student,brett-morgan.weebly.com,Weebly,"Biogeography, spatial modeling, insects"
Catherine Alves,@calves06,calves06@live.unc.edu,Grad student,www.catherinelalves.com,Weebly,"Coral reef ecology, fisheries management, marine conservation"
Emily Judd,@go4launchemily,emily.l.judd@gmail.com,Grad Student,https://emilyljudd.space,weebly,Space science/engineering
Erin Siracusa,@erin_sira,erinsiracusa@gmail.com,Grad student,https://erinsiracusa.weebly.com/,Weebly,Behavioural Ecology
Ines Barreiros,@inesvbarreiros,ines.barreiros@chch.ox.ac.uk,Grad Student,http://inesvbarreiros.weebly.com/,weebly,Neuroscience
Isabella Oleksy,@isabella_oleksy,bellaoleksy@gmail.com,Grad Student,http://isabellaoleksy.weebly.com,Weebly,Ecosystem ecology
Janice Love,@Txin2016,jlove5@nd.edu,Grad Student,https://janicemlove.weebly.com,weebly,Developmental biology
Lauren Rowsey,@rowdyscience,lrowsey@unb.ca,Grad Student,laurenrowsey.weebly.com,Weebly,"Fish ecophysiology, winter dormancy "
Maureen Williams,@modubs11,william2@tcd.ie,Grad Student,maureenannewilliams.weebly.com ,Weebly,"Parasites, ecology, biology"
Rebecca Abney ,@RebeccaAbney12,rebabney@iu.edu,Post Doc ,https://rebeccaabney.weebly.com/,Weebly,Soil biogeochemistry; heterogeneous atmospheric chemistry
Samniqueka Halsey ,@Samniqueka_H,Samniquekahalsey@gmail.com ,Grad Student,Samniquekahalsey.com,Weebly,"Computational ecology,disease ecology, plant conservation "
Theresa Barosh,@cecidologists,theresa.barosh@gmail.com ,Grad student,theresabarosh.weebly.com ,weebly,"herbivory, science communication"
Allison Roessler,@allisonroessler,kellyalg@umich.edu,Grad Student,https://www.allisonroessler.com/,Wix,Computational Chemistry (polymer mechanochemistry)
Allison Towner,--,at4bu@virginia.edu,Grad Student,https://apmtowner.wixsite.com/home,Wix,"Astronomy, Radio Astronomy (massive star formation)"
Amy Nusbaum,@amy_nusbaum,amy.nusbaum@wsu.edu,Grad Student,https://amynusbaum.wixsite.com/atnusbaum,Wix,Cognitive psychology
Carolyn Chlebek,@carolyn_chlebek,Carolyn.chlebek@gmail.com,Grad Student,https://carolynchlebek.wixsite.com/mysite,Wix,Biomedical Engineering: orthopaedic biomechanics
Evan Brooks,@ecbrooks96,evan.brooks@cchmc.org,Grad Student,https://ecbrooks1996.wixsite.com/ecbrooks,Wix,Developmental biology
Mallarie Yeager,@mallarie_yeager,yeager.m@husky.neu.edu,Grad Student,https://mallarieyeager1.wixsite.com/mysite,Wix,"Marine community ecology, functional diversity, spatial processes "
Michelle Sugimoto,,msugi@bu.edu,Grad Student,michellesugimoto.wixsite.com/research,wix,Materials Science (clean energy applications)
Sam Turley,@samaboutspace,STurley2@mail.depaul.edu,Grad Student,https://samturley.com/,Wix,Human-computer interaction
Akacia Halliday,@kcthescientist,akacia.halliday@gmail.com,Grad student,www.akaciahalliday.wordpress.com,Wordpress,Biological Sciences
Andrea Haverkamp,--,haverkaa@oregonstate.edu,Grad Student,https://sjengineers.blog/,Wordpress,"Engineering Education, Diversity & Inclusion, Feminist Research Methods"
Cecilia Klauber,@ceciklauber,Cecilia.Klauber@gmail.com,Grad Student,www.cecilia-klauber.com,Wordpress,Electrical Engineering: power and energy systems
Christiana McDonald-Spicer,@christianams,christiana.mcdonald-spicer@anu.edu.au,Grad Student,https://christianamcdonaldspicer.wordpress.com/,Wordpress,"Biogeography, macroecology, herpetology"
Christopher Berry,@cplberry,cplb@star.sr.bham.ac.uk,Post Doc,http://cplberry.com,Wordpress,Gravitational-wave astronomy
Hannah Dahlberg-Dodd@hedahlbergdodd,,dahlberg-dodd.1@osu.edu,Grad Student,http://hedahlbergdodd.com,Wordpress,"Linguistics (Japanese sociocultural ling, media studies)"
Meridith Lauren Bartley,@AlwaysScientist,Bartley@psu.edu,Grad Student,Www.MLBartley.com,Wordpress,Statistics (Ecological research focus)
Rachel Renbarger,@raytchulleigh,rachelrenbarger@gmail.com,Grad Student,rachelrenbarger.wordpress.com,Wordpress,Educational Psychology
Ritu Raman,@DrRituRaman,ritur@mit.edu,Post Doc,www.rituraman.com,Wordpress,
Sarah Parker,@_scientistsarah ,sarahparker42296@gmail.com ,Grad Student,sarahparkerastro.com,Wordpress,extragalactic astronomy
Tabitha Moses,@back2brains,tabitha.moses@gmail.com,Grad Student,www.tabithamoses.com,Wordpress,"Substance use (humans), mental health, neuroethics, bioethics"
Vincent Medina,@vincentamedina,vmedin2@lsu.edu,Grad Student,https://vincentamedina.com,Wordpress,Cognitive and Brain Sciences
Lee Taber,@lee_taber,ltaber@ucsc.edu,Grad Student,leetaber.com,Wordpress,HCI: Self-Presentation through Media
Adrian Sanborn,,asanborn@stanford.edu,Grad Student,http://www.adriansanborn.com/,,
Amy Cheu,@BasiliskosArt,amy@basiliskos.com,Grad Student,www.Basiliskos.com,,"Evolutionary functional morphology and biomechanics, Scientific illustration"
Anna Wright,@anchwr,awright@physics.rutgers.edu,Grad student,http://www.ashleedauphinais.com/,,Astrophysics (galaxies)
Benjamin Blanchard,@BenDBlanchard,bblanchard@uchicago.edu,Grad Student,https://benjaminblanchard.net,,"Morphological evolution, ants, diversification, ants, functional traits, more ants"
Caitlan Truelove,@brainyviolinist,trueloce@mail.uc.edu,Grad Student,caitlantruelove.com,,
David Baranger,@DABaranger,dbaranger@gmail.com,Grad Student,https://davidbaranger.com/,,
Donta Council,@dontacouncil,dcoun004@odu.edu,Grad Student,https://student.wp.odu.edu/dcoun004/,,Public Administration & Policy
Giuliana Viglione,@GAViglione,viglione.ga@gmail.com,Grad Student,https://www.giulianaviglione.com,,Physical oceanography/climate science/polar science
Kelsey Wood,@klsywd,klsywd@gmail.com,Grad Student,www.kelseywood.com,,
Kris Sabbi,@KrisSabbi,ksabbi@unm.edu,Grad Student,krissabbi.com,,Chimpanzee hormonal and social development
Michael Studivan,@theMikeAquatic,studivanms@gmail.com,Post Doc,mesophoticmike.weebly.com,,Mesophotic coral reef ecology
Muhammad Shamim,@sa501428,mshamim@bcm.edu,Grad Student,http://mshamim.com/,,
Natalie McKirdy,@nat_mac26,mcnerdy.science@gmail.com,Grad Student,www.nataliemckirdy.com,,Biomaterial engineering/retinal implants/medical science
Nicole Barbaro,@NicoleBarbaro,nmbarbar@oakland.edu,Grad Student,www.nicolebarbaro.com,,Evolutionary Psychology (Pubertal development; attachment; behavioral genetics)
Oliver Stringham,@OliverStringham,Oliverstringham@gmail.com,Grad student ,www.oliverstringham.com,,Conservation ecology 
Samuel Ross,@SamRPJRoss,s.ross.res@outlook.com,Grad Student,https://srpjr.wordpress.com/,,"Community ecology, global change, ecological stability etc."
Sanjit Singh Batra,@sanjitsbatra,sanjitsbatra@gmail.com,Grad Student,http://sanjitsbatra.com/,,
Sara Cannon,@secanno,secanno@gmail.com,Grad Student,http://saraecannon.com,,"marine biology, coral reef studies"
Sarah Winnicki,@skwinnicki,skwinnicki@ksu.edu,Grad Student,www.sarahwinnicki.com,,"avian ecology, nestling development, cowbird parasitism, grassland songbirds"
Stepfanie Aguillon,@s_m_aguillon,sma256@cornell.edu,Grad Student,www.stepfanieaguillon.com,,
Suhas Rao,@ThisIsSuhas,suhas@suhasrao.com,Grad Student,http://suhasrao.com/,,
Sukrit Singh,@sukritsingh92,sukrit.singh@wustl.edu,Grad Student,https://sukritsingh.github.io/,,
Ved Topkar,@vedtopkar,vedtopkar@gmail.com,Grad Student,vedtopkar.com,,
"""
def toURL():
    global csv_data
    # Use io.StringIO to treat the string as a file-like object
    file_like_object = io.StringIO(csv_data)
    # Create a csv reader
    reader = csv.reader(file_like_object)
    # Skip the header row
    next(reader)
    # Initialize a list to store the values from the fifth column
    fifth_column = []
    # Iterate over the rows in the CSV data
    for row in reader:
        # Append the value from the fifth column to the list
        if len(row) >= 5:  # Ensure there are at least 5 columns in the row
            fifth_column.append(row[4])
    # Return the values from the fifth column
    return fifth_column
def toEmail():
    global csv_data
    # Use io.StringIO to treat the string as a file-like object
    file_like_object = io.StringIO(csv_data)
    # Create a csv reader
    reader = csv.reader(file_like_object)
    # Skip the header row
    next(reader)
    # Initialize a list to store the values from the third column
    third_column = []
    # Iterate over the rows in the CSV data
    for row in reader:
        # Append the value from the third column to the list
        if len(row) >= 3:  # Ensure there are at least 3 columns in the row
            third_column.append(row[2])
    # Return the values from the third column
    return third_column
