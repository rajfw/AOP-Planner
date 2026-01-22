# AOP Planner - User Guide

## Getting Started

### First Time Login

1. Navigate to the application URL
2. Click **"Sign in with Google"**
3. Authorize the application
4. You'll be logged in as a **Requester** by default

### User Roles

#### Requester
- Create and submit roadmap requests
- Upload and manage PRDs
- Use AI-powered PRD improvement tools
- View your own submissions

#### Reviewer
- All Requester capabilities
- Review submitted roadmap requests
- Provide feedback on requests

#### Admin
- All Reviewer capabilities
- Manage users and roles
- Configure roadmap request forms
- Load sample data
- Access admin panel

## Features Guide

### 1. PRD Management

#### Uploading a PRD

1. Click **"PRD Tool"** from the navigation
2. Click **"Upload PRD"**
3. Select your file (supports: TXT, PDF, DOC, DOCX, MD)
4. Wait for parsing to complete
5. Review the extracted content

#### Improving a PRD with AI

1. After uploading or editing a PRD
2. Click **"Improve with AI"**
3. Choose improvement type:
   - **Comprehensive**: Full enhancement with all sections
   - **Clarify**: Simplify and remove ambiguity
   - **Expand**: Add more details and depth
4. Review AI suggestions
5. Accept or edit as needed

#### Analyzing a PRD

1. Click **"Analyze"** button
2. View completeness score
3. Review RICE analysis:
   - **Reach**: Number of users affected
   - **Impact**: Value to users (0.25-3.0)
   - **Confidence**: Certainty percentage
   - **Effort**: Person-months required
4. Check missing sections
5. Follow recommendations

#### Using the AI Assistant

1. Click the **chat icon** in the PRD editor
2. Ask questions like:
   - "Help me write the success metrics section"
   - "What's missing from this PRD?"
   - "Suggest user stories for this feature"
3. The assistant has context of your current PRD
4. Copy suggestions into your document

#### Exporting a PRD

1. Click **"Export"**
2. Choose format:
   - **Markdown (.md)**: For version control
   - **Word (.docx)**: For sharing with stakeholders
3. File downloads automatically

### 2. Roadmap Planning

#### Creating a Roadmap Request

1. Click **"Roadmap Planner"** from navigation
2. Click **"New Request"**
3. Fill out the multi-step form:

**Step 1: Basic Information**
- Title: Clear, descriptive name
- Description: Detailed explanation
- Business Unit: Select your BU
- Target Year: Planning year

**Step 2: Timeline**
- Half Year: H1 or H2
- Quarter: Specific quarter (auto-filtered based on half)

**Step 3: Feature Details**
- Feature Type:
  - **Hero Big Rock**: Major strategic initiative
  - **Big Rock**: Significant feature
  - **Small Rock**: Minor enhancement
- Business Impact: Rate 1-5 (5 = highest)

**Step 4: Dependencies & Attachments**
- Add dependencies on other features
- Upload PRD document
- Upload mockups/designs

4. Click **"Submit"**

#### Viewing Roadmap Requests

1. Dashboard shows all requests
2. Use filters:
   - **Business Unit**: Filter by BU
   - **Quarter**: Filter by timeline
   - **Status**: Draft, Submitted, Approved
3. Click on any request to view details

#### Editing a Request

1. Find your request in the dashboard
2. Click **"Edit"**
3. Modify any fields
4. Save changes

#### Deleting a Request

1. Find your request
2. Click **"Delete"**
3. Confirm deletion
4. Associated files are also removed

### 3. Admin Functions

#### Accessing Admin Panel

1. Login as admin user
2. Click **"Admin"** in navigation
3. Admin dashboard opens

#### Managing Users

1. Go to **"User Management"** tab
2. View all users
3. Edit user roles:
   - Change role dropdown
   - Click **"Update"**
4. Delete users (use with caution)

#### Configuring Forms

1. Go to **"Form Configuration"** tab
2. Modify form fields:
   - Add new fields
   - Change dropdown options
   - Set required fields
   - Reorder fields
3. Click **"Save Configuration"**
4. Changes apply immediately to new requests

#### Loading Sample Data

1. Go to **"Data Management"** tab
2. Click **"Load Sample Data"**
3. Confirms loading of demo roadmap requests
4. Use for testing or demonstrations

## Tips & Best Practices

### Writing Better PRDs

1. **Be Specific**: Avoid vague language
2. **Include Metrics**: Define success criteria
3. **User-Focused**: Write from user perspective
4. **Complete Sections**: Fill all PRD sections
5. **Use AI Wisely**: Review AI suggestions critically

### Roadmap Planning

1. **Clear Titles**: Use descriptive, searchable names
2. **Accurate Impact**: Be honest about business impact
3. **Track Dependencies**: Document all dependencies
4. **Attach Documents**: Include PRDs and mockups
5. **Regular Updates**: Keep requests current

### Using AI Features

1. **Provide Context**: More content = better suggestions
2. **Iterate**: Use AI multiple times to refine
3. **Review Carefully**: AI suggestions need human review
4. **Ask Specific Questions**: Get better assistant responses
5. **Save Regularly**: Don't lose your work

## Keyboard Shortcuts

- **Ctrl/Cmd + S**: Save PRD (in editor)
- **Esc**: Close modals
- **Tab**: Navigate form fields

## Troubleshooting

### "AI features not available"
- Contact admin to configure OpenAI API
- Check your internet connection

### "Upload failed"
- Check file size (max 16MB)
- Verify file type is supported
- Try a different file format

### "Cannot submit request"
- Ensure all required fields are filled
- Check file attachments are valid
- Refresh page and try again

### "Not authorized"
- Verify you're logged in
- Check if you have the required role
- Contact admin for role upgrade

### Google Login Issues
- Clear browser cookies
- Try incognito/private mode
- Verify Google account email
- Contact admin to check OAuth configuration

## FAQ

**Q: Can I edit a PRD after uploading?**
A: Yes, the editor allows full editing. Save when done.

**Q: How accurate is the RICE analysis?**
A: AI provides estimates based on PRD content. Review and adjust as needed.

**Q: Can I delete uploaded files?**
A: Yes, use the delete button in the PRD list. This is permanent.

**Q: Who can see my roadmap requests?**
A: All authenticated users can view requests. Admins can edit/delete any request.

**Q: How do I become an admin?**
A: Contact your system administrator to upgrade your role.

**Q: Can I export multiple PRDs at once?**
A: Currently, export one at a time. Batch export coming soon.

**Q: What happens to my data?**
A: Data is stored securely on the server. Regular backups are recommended.

## Getting Help

- **Technical Issues**: Contact your IT administrator
- **Feature Requests**: Submit via your organization's process
- **Bug Reports**: Document steps to reproduce and contact support

## Version Information

- **Current Version**: 1.0
- **Last Updated**: January 2026
- **Supported Browsers**: Chrome, Firefox, Safari, Edge (latest versions)
