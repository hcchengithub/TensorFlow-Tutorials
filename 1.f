import matplotlib.pyplot constant plt // ( -- module ) matplotlib.pyplot
import tensorflow constant tf // ( -- module ) TensorFlow
import numpy constant np // ( -- module ) numpy
import os constant os // ( -- module ) os
import inception constant inception // ( -- module ) Function and classes for loading and using the Inception model

ok tf :> __version__ . cr \ ==> 1.4.0

\ download inception model, current working directory is :
\ c:\Users\hcche\Documents\GitHub\TensorFlow-Tutorials\

    inception :> maybe_download()

    <comment>
    OK inception :> maybe_download()
    Downloading Inception v3 Model ...
    - Download progress: 38.3%
    ...
    - Download progress: 100.0%
    Download finished. Extracting files.
    Done.
    OK    
    </comment>
    
\ Load the inception model

    inception :> Inception() constant model // ( -- model ) The Inception v3 model 

    \ The deprecation warning from TensorFlow        
    2017-12-11 23:16:05.537612: I C:\tf_jenkins\home\workspace\rel
    -win\M\windows\PY\36\tensorflow\core\platform\
    cpu_feature_guard.cc:137] Your CPU supports instructions that 
    this TensorFlow binary was not compiled to use: AVX
    OK
    
\ Classify an image by using the inception model and 
\ print the classification scores.

    <accept>
    cr cr <text>
    c:\Users\hcche\Downloads\jeforth.3we logo 2014-10-22.jpeg
    </text>
    model :> classify(image_path=pop().strip()) cr cr 
    model :: print_scores(pred=pop(),k=10,only_first_name=True)
    </accept> dictate 
    
<comment>    


    OK ^D
    <text>
    c:\Users\hcche\Documents\GitHub\TensorFlow-Tutorials\inception\cropped_panda.jpg
    </text>
    model :> classify(image_path=pop().strip())
    model :: print_scores(pred=pop(),k=10,only_first_name=True)
    ^D
    2017-12-11 23:42:16.191967: W C:\tf_jenkins\home\workspace\rel-win\M\windows\PY\36\tensorflow\core\framework\op_def_util.cc:334] Op BatchNormWithGlobalNormalization is deprecated. It will cease to work in GraphDef version 9. Use tf.nn.batch_normalization().
    89.63% : giant panda
     0.77% : indri
     0.27% : lesser panda
     0.14% : custard apple
     0.10% : earthstar
     0.08% : sea urchin
     0.05% : forklift
     0.05% : go-kart
     0.04% : soccer ball
     0.04% : sports car
    OK

    char model py> tick(tos()) execute py: globals()[pop()]=pop()
    
model :: load("saved_networks/tflearn.lstm.model.1512226129")
import librosa constant librosa // ( -- module ) 
import numpy constant np // ( -- module )
librosa py: globals()['librosa']=pop()
np  py: globals()['np']=pop()
char librosa  glo :> [tos()] ( <var-name> glo.<var-name> ) py: globals()[pop()]=pop()
char np  glo :> [tos()] ( <var-name> glo.<var-name> ) py: globals()[pop()]=pop()
{} value y,sr // ( -- tuple ) wave file and sampling rate from librosa.load()
none value mfcc // ( -- obj ) mfcc 
"" value filename  // ( -- pathname ) .wav file 
none value MFCC // ( -- obj ) MFCC
s" c:\Users\hcche\Downloads\3-hc-a.wav" to filename
char filename filename py: globals()[pop()]=pop()
py> librosa.load(v('filename'),mono=True) to y,sr
py> librosa.feature.mfcc(v('y,sr')[0],v('y,sr')[1]) to mfcc
char mfcc mfcc py: globals()[pop()]=pop()
py> np.pad(mfcc,((0,0),(0,80-len(mfcc[0]))),mode='constant',constant_values=0) to MFCC
MFCC model :> predict([pop()]) tib.

\ T550 OA in my office
cd c:\Users\hcche\Documents\GitHub\TensorFlow-Tutorials
import matplotlib.pyplot constant plt // ( -- module ) matplotlib.pyplot
import tensorflow constant tf // ( -- module ) TensorFlow
import numpy constant np // ( -- module ) numpy
import os constant os // ( -- module ) os
tf :> __version__ tib. 

\ 我也不懂為何 import inception 非要如此，否則 error : No module named 'inception'
import sys constant sys // ( -- module )
sys :: path.append(r'c:\Users\hcche\Documents\GitHub\TensorFlow-Tutorials')
import inception constant inception // ( -- module ) Function and classes for loading and using the Inception model

</comment>    
        
    