import torch
import torch.nn as nn
import pickle


# the model_path will be specified by Anacosita Pipeline
# model will be specified by the user
def torch_model_loader(model_path: str, model: nn.Module) -> torch.nn.Module:
    model = model.load_state_dict(torch.load(model_path))
    return model.eval()

def torch_model_saver(model_path: str, model: nn.Module) -> None:
    torch.save(model.state_dict(), model_path)

def torchscript_model_loader(model_path: str, model: nn.Module) -> torch.jit.ScriptModule:
    model = torch.jit.load(model_path)
    return model.eval()

def torchscript_model_saver(model_path: str, model: nn.Module) -> None:
    # Convert the model to TorchScript
    scripted_model = torch.jit.script(model)

    # Save the TorchScript model
    scripted_model.save(model_path)

def pickle_model_loader(model_path: str) -> object:
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
        return model

def pickle_model_saver(model_path: str, model: object) -> None:
    with open(model_path, 'wb') as file:
        pickle.dump(model, file)

def custom_model_loader() -> object:
    pass

def custom_model_saver() -> None:
    pass