import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/models/commerce_models.dart';
import '../../../core/widgets/channel_status_card.dart';
import '../../../core/widgets/primary_action_button.dart';
import '../../../core/widgets/secondary_action_button.dart';
import '../../../core/theme/app_colors.dart';

/// Screen that allows an artisan to select which channels to sell a product on.
///
/// UX:
/// "Where do you want to sell this product?"
///
/// [ Craftsy ]  ✓ Selling
/// [ ONDC ]     ⚠ Needs information
/// [ Government ] ○ Not connected
class ProductChannelSelectorScreen extends ConsumerStatefulWidget {
  final String productId;

  const ProductChannelSelectorScreen({
    super.key,
    required this.productId,
  });

  @override
  ConsumerState<ProductChannelSelectorScreen> createState() =>
      _ProductChannelSelectorScreenState();
}

class _ProductChannelSelectorScreenState
    extends ConsumerState<ProductChannelSelectorScreen> {
  List<ChannelStatus> _channelStatuses = [];
  bool _isLoading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _loadChannelStatuses();
  }

  Future<void> _loadChannelStatuses() async {
    setState(() {
      _isLoading = true;
      _error = null;
    });

    try {
      // TODO: Replace with actual API call when commerce service is wired
      // final response = await ref.read(commerceServiceProvider).getChannelStatuses(widget.productId);
      await Future.delayed(const Duration(milliseconds: 500));

      // Placeholder data for now — will be replaced with real API
      _channelStatuses = [
        ChannelStatus(
          channel: 'craftsy',
          status: 'active',
          label: 'Craftsy Marketplace',
          icon: 'shopping_bag',
          color: 'indigo',
          isConnected: true,
          canPublish: false,
        ),
        ChannelStatus(
          channel: 'ondc',
          status: 'not_connected',
          label: 'ONDC',
          icon: 'public',
          color: 'teal',
          isConnected: false,
          canPublish: false,
        ),
        ChannelStatus(
          channel: 'gem',
          status: 'not_connected',
          label: 'Government Selling',
          icon: 'account_balance',
          color: 'amber',
          isConnected: false,
          canPublish: false,
        ),
      ];

      setState(() {
        _channelStatuses = _channelStatuses;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _error = e.toString();
        _isLoading = false;
      });
    }
  }

  Future<void> _publishToChannel(ChannelStatus status) async {
    // TODO: Wire to actual publish API
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('Publishing to ${status.label}...'),
        backgroundColor: AppColors.indigo,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Sell Your Craft'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => Navigator.of(context).pop(),
        ),
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _error != null
              ? _buildErrorState()
              : _buildChannelList(),
    );
  }

  Widget _buildErrorState() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Icon(Icons.error_outline, size: 48, color: AppColors.error),
          const SizedBox(height: 16),
          Text(
            'Error loading channels',
            style: Theme.of(context).textTheme.titleMedium,
          ),
          const SizedBox(height: 8),
          Text(
            _error ?? 'Unknown error',
            style: Theme.of(context).textTheme.bodySmall,
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 24),
          PrimaryActionButton(
            label: 'Retry',
            onPressed: _loadChannelStatuses,
          ),
        ],
      ),
    );
  }

  Widget _buildChannelList() {
    return Column(
      children: [
        // Header
        Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            children: [
              Text(
                'Where do you want to sell this product?',
                style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                      fontWeight: FontWeight.w600,
                    ),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 8),
              Text(
                'Choose one or more channels. You can change this later.',
                style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                      color: AppColors.textSecondary,
                    ),
                textAlign: TextAlign.center,
              ),
            ],
          ),
        ),

        // Channel cards
        Expanded(
          child: ListView.builder(
            padding: const EdgeInsets.symmetric(horizontal: 16),
            itemCount: _channelStatuses.length,
            itemBuilder: (context, index) {
              final status = _channelStatuses[index];
              return ChannelStatusCard(
                status: status,
                onTap: () => _showChannelDetails(status),
                onPublish: status.canPublish
                    ? () => _publishToChannel(status)
                    : null,
              );
            },
          ),
        ),

        // Bottom actions
        Container(
          padding: const EdgeInsets.all(24),
          child: Row(
            children: [
              Expanded(
                child: SecondaryActionButton(
                  label: 'Skip',
                  onPressed: () => Navigator.of(context).pop(),
                ),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: PrimaryActionButton(
                  label: 'Continue',
                  onPressed: () {
                    // TODO: Save channel selections and proceed
                    Navigator.of(context).pop();
                  },
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }

  void _showChannelDetails(ChannelStatus status) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (context) {
        return DraggableScrollableSheet(
          initialChildSize: 0.6,
          maxChildSize: 0.9,
          minChildSize: 0.3,
          expand: false,
          builder: (context, scrollController) {
            return SingleChildScrollView(
              controller: scrollController,
              padding: const EdgeInsets.all(24),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Handle bar
                  Center(
                    child: Container(
                      width: 40,
                      height: 4,
                      decoration: BoxDecoration(
                        color: AppColors.inkFaint,
                        borderRadius: BorderRadius.circular(2),
                      ),
                    ),
                  ),
                  const SizedBox(height: 20),

                  // Channel name
                  Text(
                    status.label,
                    style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                          fontWeight: FontWeight.w700,
                        ),
                  ),
                  const SizedBox(height: 8),

                  // Status
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 12,
                      vertical: 6,
                    ),
                    decoration: BoxDecoration(
                      color: _getStatusColor(status).withValues(alpha: 0.1),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Text(
                      status.displayStatus,
                      style: TextStyle(
                        fontSize: 14,
                        fontWeight: FontWeight.w500,
                        color: _getStatusColor(status),
                      ),
                    ),
                  ),

                  // Missing requirements
                  if (status.missingRequirements.isNotEmpty) ...[
                    const SizedBox(height: 20),
                    Text(
                      'Required Information',
                      style: Theme.of(context).textTheme.titleMedium?.copyWith(
                            fontWeight: FontWeight.w600,
                          ),
                    ),
                    const SizedBox(height: 8),
                    ...status.missingRequirements.map(
                      (field) => Padding(
                        padding: const EdgeInsets.symmetric(vertical: 4),
                        child: Row(
                          children: [
                            const Icon(
                              Icons.circle,
                              size: 8,
                              color: AppColors.amber,
                            ),
                            const SizedBox(width: 8),
                            Expanded(
                              child: Text(
                                field,
                                style: const TextStyle(fontSize: 14),
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ],

                  // Action buttons
                  const SizedBox(height: 32),
                  if (status.canPublish)
                    PrimaryActionButton(
                      label: 'Publish to ${status.label}',
                      onPressed: () {
                        Navigator.pop(context);
                        _publishToChannel(status);
                      },
                    )
                  else if (status.needsInfo)
                    PrimaryActionButton(
                      label: 'Set up ${status.label}',
                      onPressed: () {
                        Navigator.pop(context);
                        // TODO: Navigate to setup flow
                      },
                    )
                  else if (status.isNotConnected)
                    PrimaryActionButton(
                      label: 'Connect ${status.label}',
                      onPressed: () {
                        Navigator.pop(context);
                        // TODO: Navigate to connection flow
                      },
                    ),
                ],
              ),
            );
          },
        );
      },
    );
  }

  Color _getStatusColor(ChannelStatus status) {
    if (status.isLive) return AppColors.success;
    if (status.hasFailed) return AppColors.error;
    if (status.needsInfo) return AppColors.amber;
    if (status.isPending) return AppColors.indigo;
    return AppColors.inkSoft;
  }
}
