export class SlackError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'SlackError';
  }
}

export class SlackValidationError extends SlackError {
  response: any;
  
  constructor(message: string, response?: any) {
    super(message);
    this.name = 'SlackValidationError';
    this.response = response;
  }
}

export class SlackAuthenticationError extends SlackError {
  constructor(message: string) {
    super(message);
    this.name = 'SlackAuthenticationError';
  }
}

export class SlackResourceNotFoundError extends SlackError {
  constructor(message: string) {
    super(message);
    this.name = 'SlackResourceNotFoundError';
  }
}

export class SlackPermissionError extends SlackError {
  constructor(message: string) {
    super(message);
    this.name = 'SlackPermissionError';
  }
}

export class SlackRateLimitError extends SlackError {
  resetAt: Date;
  
  constructor(message: string, resetAt: Date) {
    super(message);
    this.name = 'SlackRateLimitError';
    this.resetAt = resetAt;
  }
}

export function isSlackError(error: any): error is SlackError {
  return error instanceof SlackError;
}

export function formatSlackError(error: SlackError): string {
  let message = `Slack API Error: ${error.message}`;
  
  if (error instanceof SlackValidationError) {
    message = `Validation Error: ${error.message}`;
    if (error.response) {
      message += `\nDetails: ${JSON.stringify(error.response)}`;
    }
  } else if (error instanceof SlackResourceNotFoundError) {
    message = `Not Found: ${error.message}`;
  } else if (error instanceof SlackAuthenticationError) {
    message = `Authentication Failed: ${error.message}`;
  } else if (error instanceof SlackPermissionError) {
    message = `Permission Denied: ${error.message}`;
  } else if (error instanceof SlackRateLimitError) {
    message = `Rate Limit Exceeded: ${error.message}\nResets at: ${error.resetAt.toISOString()}`;
  }

  return message;
} 