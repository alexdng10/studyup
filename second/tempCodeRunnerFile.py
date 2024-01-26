for epoch in range(1):  # Number of epochs
    total_loss = 0
    correct_predictions = 0
    total_predictions = 0

    for batch in dataloader:
        input_ids, attention_mask, labels, idx = [b.to(device) for b in batch]

        model.zero_grad()  # Reset gradients to zero
        outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
        
        loss = outputs.loss
        logits = outputs.logits
        loss.backward()  # Backpropagation
        optimizer.step()  # Update weights

        total_loss += loss.item()

        # Calculate accuracy
        predictions = torch.argmax(logits, dim=1)
        correct_predictions += (predictions == labels).sum().item()
        total_predictions += labels.size(0)

    # Calculate average loss and accuracy over the epoch
    avg_loss = total_loss / len(dataloader)
    accuracy = correct_predictions / total_predictions

    print(f"Epoch {epoch}, Loss: {avg_loss:.4f}, Accuracy: {accuracy:.4f}")