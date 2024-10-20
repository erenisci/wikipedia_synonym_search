def clean(sentence):
    
    """
    Wikipedia veriseti için preprocess işlemlerini yapan fonksiyon
    
    Input
        sentence [string] :  XML dosyasından gelen cümle
    
    Output
        sentence [string] :  Temizlenmiş cümle
    
    """
    
    
   
    
    table = str.maketrans("ABCÇDEFGĞHİIJKLMNOÖPRSŞTUÜVYZWXQ","abcçdefgğhiıjklmnoöprsştuüvyzwxq")



    
    
    # Check special char
    if "==" not in sentence and  "|" not in sentence and "!" in sentence and "ISBN" not in sentence and  ". Bölüm" not in sentence and "≈" not in sentence and "=" not in sentence and "http" not in sentence:
        
        
        sentence_ = sentence.strip().split()
        
        if sentence_[0] != "InDesign" and sentence_[0] != "Dosya" and sentence_[0] != "Image" and sentence_[0] != "YÖNLENDİRME" and sentence_[0] != "bar:" and sentence_[0] != "TextData=" and      sentence_[0] != "fontsize:" and sentence_[0] != "id" and sentence_[0] != "ImageSize" and sentence_[0] != "PlotArea" and sentence_[0] != "DateFormat" and sentence_[0] != "Period"            and sentence_[0] != "TimeAxis" and sentence_[0] != "AlignBars" and sentence_[0] != "ScaleMajor" and sentence_[0] != "ScaleMinor" and sentence_[0] != "BackgroundColors" and sentence_[0] != "BarData" and sentence_[0] != "REDIRECT" and sentence_[0] != "@":
             
        
        
            
            if len(sentence.split()) > 4:
                
                
                # Removing special characters
                sentence = sentence.replace("\n"," ").replace("\t"," ").replace("Hicrî","Hicrî ").replace("Rumi","Rumi ")
                
                
                # Lowercase
                sentence = sentence.translate(table)
            
                
                return sentence
            
    