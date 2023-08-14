from tokenizers import Tokenizer, models, pre_tokenizers, decoders, trainers, processors
from transformers import PreTrainedTokenizerFast, DataCollatorWithPadding
import os

def buildCustomTokenizer(data_path,tokenizer_path):
    # Initialize a tokenizer
    tokenizer = Tokenizer(models.BPE())
    # Use the BPE tokenizer
    tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel()
    tokenizer.decoder = decoders.ByteLevel()
    tokenizer.post_processor = processors.ByteLevel(trim_offsets=False)
    # Training from your file
    trainer = trainers.BpeTrainer(vocab_size=30000, min_frequency=2)
    tokenizer.train(files=[data_path], trainer=trainer)

    #add special tokens
    num_added = tokenizer.add_tokens(["[CLS]", "[SEP]", "[PAD]", "[UNK]", "[MASK]"])
    print(f"Number of tokens added: {num_added}")
    tokenizer.post_processor = processors.TemplateProcessing(
        single="[CLS] $A [SEP]",
        pair="[CLS] $A [SEP] $B:1 [SEP]:1",
        special_tokens=[
            ("[CLS]", tokenizer.token_to_id("[CLS]")),
            ("[SEP]", tokenizer.token_to_id("[SEP]")),
        ],
    )
    tokenizer.save(tokenizer_path)
    return tokenizer

def loadCustomTokenizer(tokenizer_path,model_max_length=512):
    tokenizer = PreTrainedTokenizerFast(
        tokenizer_file=tokenizer_path,
        model_max_length=model_max_length,
        pad_token="[PAD]",
        sep_token="[SEP]",
        cls_token="[CLS]",
        mask_token="[MASK]"
    )
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
    return tokenizer,data_collator

if __name__ == '__main__':
    print(os.getcwd())
    data_path = 'data/train-very-basic.csv'
    tokenizer_path = 'data/my_tokenizer'
    tokenizer = buildCustomTokenizer(data_path,tokenizer_path)
    tokenizer,data_collator = loadCustomTokenizer(tokenizer_path)
    #test 
    encoded = tokenizer.encode("This is a test.")
    print("Encoded:", encoded)
    decoded = tokenizer.decode(encoded)
    print("Decoded:", decoded)
    #expected output: Decoded: [CLS] This is a test[SEP]